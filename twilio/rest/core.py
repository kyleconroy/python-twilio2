import httplib2
import json
import logging
import os
import re
import urllib
import base64

try:
    from google.appengine.api import urlfetch
    from django.utils import simplejson as json
    APPENGINE = True
except:
    import httplib2
    import json
    APPENGINE = False

from urllib import urlencode 
from urlparse import urlparse, urlunparse, urljoin

def force_extension(uri, format):
    """ Force a uri to have a specfic extension """
    o = urlparse(uri)
    path, extension = os.path.splitext(o.path)
    path = path + "." + format
    o = (o.scheme, o.netloc, path, o.params, o.query, "")
    return urlunparse(o)

def force_json(uri):
    """ Force a uri to have a json extension """
    return force_extension(uri, "json")

class TwilioException(Exception): pass

class TwilioRestException(TwilioException):

    def __init__(self, status, uri, msg=""):
        self.uri = uri
        self.status = status
        self.msg = msg

    def __str__(self):
        return "HTTP ERROR %s: %s \n %s" % (self.status, self.msg, self.uri)

class Client(object):
    """
    Http Client wrapper class, so we can 
    use whatever underlying http client
    """
    
    def __init__(self, account=None, token=None, base=None):
        if account and token and base:
            self.base = base
            self.account = account
            self.token = token
            if not APPENGINE:
                self.http_client = httplib2.Http()
                self.http_client.add_credentials(account, token)
        else:
            raise TwilioException("The Wufoo API requires authentication")

    def request(self, path, method=None, d={}, xml=None):
        """sends a request and gets a response from the Twilio REST API
        path: the URL (relative to the endpoint URL, after the /v1
        url: the HTTP method to use, defaults to POST
        vars: for POST or PUT, a dict of data to send
        returns Twilio response in XML or raises an exception on error
        """

        if not path or len(path) < 1:
            raise TwilioException('Invalid path parameter')
        if method and method not in ['GET', 'POST', 'DELETE', 'PUT']:
            raise TwilioRESTException(
                'HTTP %s method not implemented' % method)
            
        uri = self.base + path

        logging.debug("%s: %s" % (method, uri))
        if xml:
            headers = {'Content-type': 'application/xml'}
            body = xml
        else:
            headers = {'Content-type': 'application/x-www-form-urlencoded'}
            body = urlencode(d)

        if APPENGINE:
            encoded = base64.b64encode(self.account + ':' + self.token)
            authstr = "Basic "+encoded
            headers['Authorization'] = authstr
            result = urlfetch.fetch(url=uri, payload=body, method=method, 
                                    headers=headers)
            content = result.content
            status = result.status_code
        else:
            resp, content = self.http_client.request(uri, method,
                                                     headers=headers, body=body)
            status = int(resp["status"])

        if status >= 300:
            try:
                logging.debug(content)
                response = json.loads(content)
                message = response["message"]
            except:
                message = ""
            raise TwilioRestException(status, uri, message)
        else:
            return content

class Resource(object):

    """An HTTP Resource"""
    def __init__(self, uri, client=None):

        self.uri = uri
        if client:
            self.client = client
        else:
            raise TwilioException, "A client is need to create a resource"

    def _get(self, path="", query={}, **kwargs):
        """Perform an HTTP GET on the requested resource"""
        qs = urllib.urlencode(query)
        uri = force_json(self.uri + path) + "?" + qs
        return self.client.request(uri, method="GET", **kwargs)
        
    def _post(self, path="", body=None, **kwargs):
        """Perform an HTTP POST on the requested resource"""
        uri = force_json(self.uri + path)
        return self.client.request(uri, method="POST", d=body, **kwargs)
        
    def _put(self, path="", **kwargs):
        """Perform an HTTP DELTE on the requested resource"""
        uri = force_json(self.uri + path)
        return self.client.request(uri, method="PUT", **kwargs)
        
    def _delete(self, path="", **kwargs):
        """Perform an HTTP DELTE on the requested resource"""
        uri = force_json(self.uri + path)
        return self.client.request(uri, method="DELETE", **kwargs)

class ListResource(Resource):

    def __init__(self, uri, name=None, **kwargs):
        self.name = name
        super(ListResource, self).__init__(uri, **kwargs)

    def create(self):
        """
        Create an InstanceResource
        ListResources must expliciity support Instance creation
        """
        raise TwilioException("InstanceResource creation not supported")

    def list(self):
        content = json.loads(self._get())
        try:
            result = []
            for item in content[self.name]:
                result.append(self._load_instance(item))
            return result
        except KeyError:
            raise TwilioException, "Key %s not present in response" % self.name

        
    def get(self, sid):
        """Request the specified instance resource"""
        content = self._get("/" + sid)
        return self._load_instance(json.loads(content))

    def _load_instance(self, d):
        return InstanceResource(self.uri, entries=d, client=self.client)

class InstanceResource(Resource):

    def __init__(self, uri, entries={}, **kwargs):
        super(InstanceResource, self).__init__(uri, **kwargs)
        result = {}
        
        # Delete conflicting parameter names
        if "from" in entries.keys():
            entries["from_"] = entries["from"]
            del entries["from"]

        self.__dict__.update(entries)
        

   
