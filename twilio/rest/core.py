import logging
import os
import re
import urllib
import base64

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
        return "HTTP ERROR {0}: {1} \n {2}".format(self.status, self.msg, self.uri)

class Resource(object):
    """An HTTP Resource"""

    def __init__(self, client, base_uri):
        self.client = client
        self.uri = "{0}/{1}".format(base_uri, self.name)

    def _request(self, uri, fmt="json", query=None, **kwargs):
        """
        Send an HTTP request to uri+fmt+query
        """
        furi = "{0}.{1}".format(uri, fmt)

        if query:
            furi = "{0}?{1}".format(furi, urllib.urlencode(query))

        resp, content = self.client.request(furi, **kwargs)
        logging.debug(resp)
        logging.debug(content)
        
        # If the HTTP request errored, throw RestException
        if resp.status >= 400:
            raise TwilioRestException(resp.status, furi, resp.reason)

        return resp, content

    def _fparam(self, p):
        """
        Filter the parameters, throwing away any None values
        """
        return dict([(d,p[d]) for d in p if p[d]])

class ListResource(Resource):

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
        uri = "{0}/{1}".format(self.uri, sid)
        resp, content =  self._request(uri, method="DELETE")
        return resp.status == 204

    def _update(self, sid, body):
        """
        Update an InstanceResource via a POST
        
        sid: string -- String identifier for the list resource
        body: string -- HTTP Body for the quest
        """
        uri = "{0}/{1}".format(self.uri, sid)
        hs = {'Content-type': 'application/x-www-form-urlencoded'}
        resp, content =  self._request(uri, method="POST", body=body, 
                                       headers=hs)
        entries = json.loads(content)
        return self._create_instance(entries)

    def count(self):
        """
        Return the number of instance resources contained in this list resource
        """
        raise TwilioException("InstanceResource count not supported")

    def _list(self, params={}):
        # Get the items
        resp, content =  self._request(self.uri, method="GET", query=params)
        page = json.loads(content)

        # Get key for the array of items
        try:
            key = self.key
        except AttributeError:
            key = self.name.lower()

        # Turn all those items into objects
        try:
            return [ self._create_instance(i) for i in page[key]]
        except KeyError:
            raise TwilioException("Key {0} not present in response".format(key))
        
    def get(self, sid):
        """Request the specified instance resource"""
        uri = "{0}/{1}".format(self.uri, sid)
        resp, content =  self._request(uri, method="GET")
        return self._create_instance(json.loads(content))

    def _create_instance(self, content):
        try:
            return self.instance(self, self.uri, content)
        except AttributeError:
            raise TwilioException("ListResource missing self.instance")

class InstanceResource(Resource):

    id_key = "sid"

    def __init__(self, list_resource, base_uri, entries):
        
        self.list_resource = list_resource

        try:
            self.name = entries[self.id_key]
        except KeyError:
            msg = "Key {0} not present in content".format(self.id_key)
            raise TwilioException(msg)

        super(InstanceResource, self).__init__(None, base_uri)
        
        # Delete conflicting parameter names
        self._load(entries)

    def _load(self, entries):
        if "from" in entries.keys():
            entries["from_"] = entries["from"]
            del entries["from"]
            
        if "uri" in entries.keys():
            del entries["uri"]

        self.__dict__.update(entries)

    def _update(self, **kwargs):
        a = self.list_resource.update(self.sid, **kwargs)
        self._load(a.__dict__)

    def _delete(self, **kwargs):
        self.list_resource.delete(self.sid, **kwargs)
