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

    def __init__(sexlf, status, uri, msg=""):
        self.uri = uri
        self.status = status
        self.msg = msg

    def __str__(self):
        return "HTTP ERROR %s: %s \n %s" % (self.status, self.msg, self.uri)

class Resource(object):

    """An HTTP Resource"""
    def __init__(self, client, base_uri):
        self.client = client
        self.uri = "{0}{1}".format(base_uri, self.name)

    def _request(self, uri, **kwargs):
        return self.client.request(uri, **kwargs)


class ListResource(Resource):

    def create(self):
        """
        Create an InstanceResource
        ListResources must expliciity support Instance creation
        """
        raise TwilioException("InstanceResource creation not supported")

    def count(self):
        """
        Return the number of instance resources contained in this list resource
        """
        raise TwilioException("InstanceResource count not supported")

    def list(self, **kwargs):
        
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
        raise TwilioException("NOT IMPLEMENTED")

    def _create_instance(self, entries):
        try:
            return self.instance(self.client, self.uri, entries)
        except AttributeError:
            raise TwilioException("ListResource missing self.instance")

class InstanceResource(Resource):

    id_key = "sid"

    def __init__(self, client, base_uri, content):

        entries = json.loads(content)
        self.name = entries[self.id_key]

        super(InstanceResource, self).__init__(client, base_uri)
        
        # Delete conflicting parameter names
        if "from" in entries.keys():
            entries["from_"] = entries["from"]
            del entries["from"]

        self.__dict__.update(entries)
