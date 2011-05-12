import logging
import os
import re
import urllib
import base64
import datetime

# import json
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json

class TwilioException(Exception): pass

class TwilioRestException(TwilioException):

    def __init__(self, status, uri, msg=""):
        self.uri = uri
        self.status = status
        self.msg = msg

    def __str__(self):
        return "HTTP ERROR %s: %s \n %s" % (self.status, self.msg, self.uri)

def fparam(p):
    """
    Filter the parameters, throwing away any None values
    """
    return dict([(d,p[d]) for d in p if p[d] is not None])

def parse_date(d):
    """
    Return a string representation of a date that the Twilio API understands
    Format is YYYY-MM-DD. Returns None if d is not a string, datetime, or date
    """
    if isinstance(d, datetime.datetime):
        return str(d.date())
    elif isinstance(d, datetime.date):
        return str(d)
    elif isinstance(d, str):
        return d

def convert_case(s):
    """
    Given a string in snake case, conver to CamelCase
    """
    return ''.join([a.title() for a in s.split("_") if a])

def convert_keys(d):
    """
    Return a dictionary with all keys converted from arguments
    """
    special = {
        "started_before": "StartTime<",
        "started_after":  "StartTime>",
        "started":        "StartTime",
        "ended_before":   "EndTime<",
        "ended_after":    "EndTime>",
        "ended":          "EndTime",
        "from_":          "From",
    }

    result = {}

    for k,v in d.iteritems():
        if k in special:
            result[special[k]] = v
        else:
            result[convert_case(k)] = v
    return result

def normalize_dates(myfunc):
    def inner_func(*args, **kwargs):
        for k, v in kwargs.iteritems():
            res = [ True for s in ["after", "before", "on"] if s in k]
            if len(res):
                kwargs[k] = parse_date(v)
        return myfunc(*args, **kwargs)
    return inner_func

class Resource(object):
    """An HTTP Resource"""

    def __init__(self, client, base_uri):
        self.client = client
        self.uri = "%s/%s" % (base_uri, self.name)

    def _request(self, uri, fmt="json", query=None, **kwargs):
        """
        Send an HTTP request to uri+fmt+query
        """
        furi = "%s.%s" % (uri, fmt)

        if query:
            furi = "%s?%s" % (furi, urllib.urlencode(query))

        headers = kwargs.get("headers", {})
        headers["User-Agent"] = "twilio-python/3.0.0"
        kwargs["headers"] = headers

        resp, content = self.client.request(furi, **kwargs)
        logging.debug(resp)
        logging.debug(content)

        # If the HTTP request errored, throw RestException
        if resp.status >= 400:
            try:
                error = json.loads(content)
                message = "%s: %s" % (error["code"], error["message"])
            except:
                message = resp.reason
            raise TwilioRestException(resp.status, furi, message)

        return resp, content

class ListResource(Resource):

    def __init__(self, *args, **kwargs):
        super(ListResource, self).__init__(*args, **kwargs)
        try:
            self.key
        except AttributeError:
            self.key = self.name.lower()

    def _create(self, body):
        """
        Create an InstanceResource via a POST to the List Resource

        body: string -- HTTP Body for the quest
        """
        hs = {'Content-type': 'application/x-www-form-urlencoded'}
        resp, content =  self._request(self.uri, method="POST", body=body,
                                       headers=hs)

        if resp.status != 201:
            raise TwilioRestException(resp.status, self.uri, "Resource not created")

        entries = json.loads(content)
        return self._create_instance(entries)

    def _delete(self, sid):
        """
        Delete an InstanceResource via DELETE

        body: string -- HTTP Body for the quest
        """
        uri = "%s/%s" % (self.uri, sid)
        resp, content =  self._request(uri, method="DELETE")
        return resp.status == 204

    def _update(self, sid, body):
        """
        Update an InstanceResource via a POST

        sid: string -- String identifier for the list resource
        body: string -- HTTP Body for the quest
        """
        uri = "%s/%s" % (self.uri, sid)
        hs = {'Content-type': 'application/x-www-form-urlencoded'}
        resp, content =  self._request(uri, method="POST", body=body,
                                       headers=hs)
        entries = json.loads(content)
        return self._create_instance(entries)

    def count(self):
        """
        Return the number of instance resources contained in this list resource
        """
        resp, content =  self._request(self.uri, method="GET")
        page = json.loads(content)
        return page["total"]

    def _list(self, params={}, page=None, page_size=None):
        # Get the items
        if page is not None:
            params["Page"] = page
        if page_size is not None:
            params["PageSize"] = page_size
        resp, content =  self._request(self.uri, method="GET", query=params)
        page = json.loads(content)

        # Get key for the array of items

        # Turn all those items into objects
        try:
            return [ self._create_instance(i) for i in page[self.key]]
        except KeyError:
            raise TwilioException("Key %s not present in response" % self.key)

    def iter(self, **kwargs):
        """
        Return all instance resources using an iterator
        Can only be called on classes which implement list()
        """
        p = 0
        try:
            while True:
                for r in self.list(page=p, **kwargs):
                    yield r
                p += 1
        except TwilioRestException:
            pass


    def _get(self, uri):
        """Request the specified instance resource"""
        resp, content =  self._request(uri, method="GET")
        return self._create_instance(json.loads(content))

    def get(self, sid):
        """Request the specified instance resource"""
        uri = "%s/%s" % (self.uri, sid)
        return self._get(uri)

    def _create_instance(self, content):
        try:
            return self.instance(self, self.uri, content)
        except AttributeError:
            raise TwilioException("%s missing self.instance" % self.name)

class InstanceResource(Resource):

    id_key = "sid"
    subresources = []

    def __init__(self, list_resource, base_uri, entries):

        self.list_resource = list_resource

        try:
            self.name = entries[self.id_key]
        except KeyError:
            msg = "Key %s not present in content" % (self.id_key)
            raise TwilioException(msg)

        super(InstanceResource, self).__init__(None, base_uri)

        # Delete conflicting parameter names
        self._load(entries)
        self._load_subresources()

    def _load(self, entries):
        if "from" in entries.keys():
            entries["from_"] = entries["from"]
            del entries["from"]

        if "uri" in entries.keys():
            del entries["uri"]

        self.__dict__.update(entries)

    def _load_subresources(self):
        client = self.list_resource.client
        for r in self.subresources:
            ir = r(client, self.uri)
            self.__dict__[ir.key] = ir

    def _update(self, **kwargs):
        a = self.list_resource.update(self.name, **kwargs)
        self._load(a.__dict__)

    def _delete(self, **kwargs):
        self.list_resource.delete(self.name, **kwargs)
