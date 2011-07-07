"""
Test the base Resource class
"""
from nose.tools import assert_equals
from nose.tools import raises
from twilio.rest.resources import Resource
from twilio.rest.resources import ListResource
from twilio.rest.resources import InstanceResource

base_uri = "https://api.twilio.com"
version = "2010-04-01"
account_sid = "AC123"
auth = (account_sid, "token")


def test_resource_init():
    auth = (account_sid, "token")
    r = Resource(base_uri, version, auth)
    uri = "{}/{}/Accounts/{}/{}".format(base_uri, version, account_sid, r.name)

    assert_equals(r.base_uri, base_uri)
    assert_equals(r.auth, auth)
    assert_equals(r.version, version)
    assert_equals(r.uri, uri)

def test_list_resource_init():
    auth = (account_sid, "token")
    r = ListResource(base_uri, version, auth)
    uri = "{}/{}/Accounts/{}/{}".format(base_uri, version, account_sid, r.name)

    assert_equals(r.uri, uri)
    assert_equals(r.key, r.name.lower())

def test_instance_resource_init():
    parent = ListResource(base_uri, version, auth)
    r = InstanceResource(parent, "123")
    uri = "%s/%s" % (parent.uri, "123")

    assert_equals(r.uri, uri)


