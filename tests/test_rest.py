import json
import os
import unittest
from datetime import datetime
from datetime import date

from mock import patch
from mock import Mock
from twilio.rest.resources import *
from twilio.rest.client import TwilioClient
from twilio.rest.core import TwilioException
from twilio.rest.core import TwilioRestException
from twilio.rest.core import InstanceResource

ACCOUNT_SID = "AC111111111"
AUTH_TOKEN  = "AUTH_TOKEN"
BASE_URI    = "https://api.twilio.com/2010-04-01/"
ACCOUNT_URI = "{0}Accounts/{1}/".format(BASE_URI, ACCOUNT_SID)

def create_mock_request(status=200, content="{}"):
    request = Mock()
    resp = Mock()
    resp.status = status
    resp.reason = "CREATED"
    request.return_value = resp, content
    return request

class ClientTest(unittest.TestCase):

    def test_creation(self):
        c = TwilioClient(account=ACCOUNT_SID, token=AUTH_TOKEN)
        self.assertEquals(c.account_sid, ACCOUNT_SID)
        self.assertEquals(c.auth_token, AUTH_TOKEN)

    def test_creation_env_variables(self):
        creds = {
            "TWILIO_ACCOUNT_SID": ACCOUNT_SID,
            "TWILIO_AUTH_TOKEN": AUTH_TOKEN,
            }
        
        with patch.dict(os.environ, creds):
            c = TwilioClient()

        self.assertEquals(c.account_sid, ACCOUNT_SID)
        self.assertEquals(c.auth_token, AUTH_TOKEN)

    def test_credential_adding(self):
        client = Mock()
        client.add_credentials = Mock()
        c = TwilioClient(account=ACCOUNT_SID, token=AUTH_TOKEN, client=client)
        
        client.add_credentials.assert_called_with(ACCOUNT_SID, AUTH_TOKEN)

    def test_creation_fails(self):
        with self.assertRaises(TwilioException) as cm:
            with patch.dict(os.environ, {}, clear=True):
                c = TwilioClient()

class ResourceTest(unittest.TestCase):

    def setUp(self):
        mock_http, request, self.resp = Mock(), Mock(), Mock()
        request.return_value = self.resp, ""
        mock_http.request = request
        self.c = TwilioClient(account=ACCOUNT_SID, token=AUTH_TOKEN, 
                              client=mock_http)
        
    def test_not_found(self):
        self.resp.status = 404
        self.resp.description = "NOT FOUND"
        with self.assertRaises(TwilioRestException) as cm:
            self.c.accounts.create(friendly_name="MyNewAccount")

    def test_auth_required(self):
        self.resp.status = 401
        self.resp.description = "AUTH REQUIRED"
        with self.assertRaises(TwilioRestException) as cm:
            self.c.accounts.create(friendly_name="MyNewAccount")

class AccountsTest(unittest.TestCase):
    
    def setUp(self):
        self.mock_http = Mock()
        self.c = TwilioClient(account=ACCOUNT_SID, token=AUTH_TOKEN, 
                              client=self.mock_http)

    def test_uri(self):
        uri = "{0}Accounts".format(BASE_URI)
        self.assertEquals(self.c.accounts.uri, uri)

    def test_create_wrong_arg(self):
        with self.assertRaises(TypeError) as cm:
            a = self.c.accounts.create()

    def test_create(self):

        account_name = "SubAccount Created at 2011-02-10 16:19 pm"

        with open("tests/content/create_account.json") as f:
            content = f.read()

        request = create_mock_request(201, content)
        self.mock_http.request = request

        c = self.c.accounts.create(friendly_name=account_name)

        entries = json.loads(content)
        self.assertEquals(c.friendly_name, account_name)
        self.assertEquals(c.sid, entries["sid"])
        self.assertEquals(c.date_created, entries["date_created"])
        self.assertEquals(c.date_updated, entries["date_updated"])
        self.assertEquals(c.status, entries["status"])
        self.assertEquals(c.auth_token, entries["auth_token"])

    def test_get_uri(self):

        account_sid = "AC4bf2dafb92341f7caf8650403e422d23"
        expected_uri = "{0}Accounts/{1}.json".format(BASE_URI,account_sid)

        request = create_mock_request()
        self.mock_http.request = request

        with self.assertRaises(TwilioException) as cm:
            c = self.c.accounts.get(account_sid)

        request.assert_called_with(expected_uri, method="GET")

    def test_list_uri(self):

        expected_uri = "{0}Accounts.json".format(BASE_URI)

        request = create_mock_request()
        self.mock_http.request = request

        
        with self.assertRaises(TwilioException) as cm:
            c = self.c.accounts.list()

        request.assert_called_with(expected_uri, method="GET")

    def test_list_uri_filter(self):

        expected_uri = "{0}Accounts.json?FriendlyName=You&Status=active".format(BASE_URI)

        request = create_mock_request()
        self.mock_http.request = request

        
        with self.assertRaises(TwilioException) as cm:
            c = self.c.accounts.list(friendly_name="You", status="active")

        request.assert_called_with(expected_uri, method="GET")

    def test_update_uri(self):
        account_sid = "AC4bf2dafb92341f7caf8650403e422d23"
        expected_uri = "{0}Accounts/{1}.json".format(BASE_URI, account_sid)

        request = create_mock_request()
        self.mock_http.request = request
        
        with self.assertRaises(TwilioException) as cm:
            c = self.c.accounts.update(account_sid, friendly_name="You")

        body = "FriendlyName=You"
        hs = {'Content-type': 'application/x-www-form-urlencoded'}
        request.assert_called_with(expected_uri, method="POST", body=body, 
                                   headers=hs)

    def test_instance_update_uri(self):
        account_sid = "AC4bf2dafb92341f7caf8650403e422d23"
        base_uri = "{0}Accounts".format(BASE_URI)
        expected_uri = "{0}Accounts/{1}.json".format(BASE_URI, account_sid)

        request = create_mock_request()
        self.mock_http.request = request
        
        a = Account(self.c.accounts, base_uri, {"sid": account_sid})

        with self.assertRaises(TwilioException) as cm:
            c = a.update(friendly_name="You")

        body = "FriendlyName=You"
        hs = {'Content-type': 'application/x-www-form-urlencoded'}
        request.assert_called_with(expected_uri, method="POST", body=body, 
                                   headers=hs)

        with open("tests/content/create_account.json") as f:
            content = f.read()

    def test_instance_update(self):
        account_sid = "AC4bf2dafb92341f7caf8650403e422d23"
        base_uri = "{0}Accounts".format(BASE_URI)
        expected_uri = "{0}Accounts/{1}.json".format(BASE_URI, account_sid)

        with open("tests/content/create_account.json") as f:
            c = f.read()

        request = create_mock_request(content=c)
        self.mock_http.request = request
        
        a = Account(self.c.accounts, base_uri, {"sid": account_sid})
        a.update(friendly_name="You")

        self.assertEquals(a.date_created, "Fri, 11 Feb 2011 00:19:37 +0000")

    def test_close_uri(self):
        account_sid = "AC4bf2dafb92341f7caf8650403e422d23"
        expected_uri = "{0}Accounts/{1}.json".format(BASE_URI, account_sid)

        request = create_mock_request()
        self.mock_http.request = request
        
        with self.assertRaises(TwilioException) as cm:
            c = self.c.accounts.close(account_sid)

        body = "Status=closed"
        hs = {'Content-type': 'application/x-www-form-urlencoded'}
        request.assert_called_with(expected_uri, method="POST", body=body, 
                                   headers=hs)

    def test_request(self):
        request = create_mock_request(status=201)
        self.mock_http.request = request
        self.c.accounts._create_instance = Mock()

        self.c.accounts.create(friendly_name="MyNewAccount")

        uri = "{0}.json".format(self.c.accounts.uri)
        body = "FriendlyName=MyNewAccount"
        hs = {'Content-type': 'application/x-www-form-urlencoded'}
        request.assert_called_with(uri, method="POST", body=body, headers=hs)

    def test_instance_creation(self):

        with open("tests/content/create_account.json") as f:
            content = f.read()

        entries = json.loads(content)

        print self.c.accounts.instance
        a = self.c.accounts._create_instance(entries)

        uri = "{0}Accounts/{1}".format(BASE_URI, entries["sid"])
        self.assertEquals(a.sid, entries["sid"])
        self.assertEquals(a.uri, uri)
        self.assertEquals(a.date_created, entries["date_created"])
        self.assertEquals(a.date_updated, entries["date_updated"])
        self.assertEquals(a.status, entries["status"])
        self.assertEquals(a.auth_token, entries["auth_token"])


class AccountTest(unittest.TestCase):

    ct = {'Content-type': 'application/x-www-form-urlencoded'}

    def setUp(self):
        self.mock_http = Mock()
        self.c = TwilioClient(account=ACCOUNT_SID, token=AUTH_TOKEN, 
                              client=self.mock_http)

        self.account_sid = "AC4bf2dafb92341f7caf8650403e422d23"
        self.base_uri = "{0}Accounts".format(BASE_URI)
        self.expected_uri = "{0}Accounts/{1}.json".format(BASE_URI, 
                                                          self.account_sid)
        self.account =  Account(self.c.accounts, self.base_uri, {"sid": self.account_sid})


    def _validate(self, func, content_path, status):
        with open(content_path) as f:
            request = create_mock_request(content=f.read())
            self.mock_http.request = request

        func()

        request.assert_called_with(self.expected_uri, method="POST", 
                                   body="Status={0}".format(status), 
                                   headers=self.ct)

        self.assertEquals(self.account.status, status)

    def test_close(self):
        self._validate(self.account.close, "tests/content/close_account.json",
                       Account.CLOSED)

    def test_suspend(self):
        self._validate(self.account.suspend, "tests/content/suspend_account.json",
                       Account.SUSPENDED)

    def test_activate(self):
        self._validate(self.account.activate, "tests/content/create_account.json",
                       Account.ACTIVE)


class CallsTest(unittest.TestCase):

    def setUp(self):
        self.c = TwilioClient(account=ACCOUNT_SID, token=AUTH_TOKEN)

    def mock_request(self, status=200, content="{}"):
        request = Mock()
        resp = Mock()
        resp.status = status
        resp.reason = "CREATED"
        request.return_value = resp, content
        self.c.client.request = request
        return request

    def test_uri(self):
        uri = "{0}Calls".format(ACCOUNT_URI)
        self.assertEquals(self.c.calls.uri, uri)

    def test_get_uri(self):
        csid = "CA12312313"
        e_uri = "{0}Accounts/{1}/Calls/{2}.json".format(BASE_URI, 
                                                        ACCOUNT_SID, csid)
        request = self.mock_request()
        
        with self.assertRaises(TwilioException) as cm:
            c = self.c.calls.get(csid)

        request.assert_called_with(e_uri, method="GET")

    def test_list_uri(self):
        query = "EndTime%3C=2009-01-31&StartTime%3E=2009-01-01&EndTime=2009-12-12"
        e_uri = "{0}Accounts/{1}/Calls.json?{2}".format(BASE_URI, ACCOUNT_SID, 
                                                        query)
        request = self.mock_request()
        
        with self.assertRaises(TwilioException) as cm:
            c = self.c.calls.list(ended=date(2009,12,12), 
                                  started_after="2009-01-01",
                                  ended_before=datetime(2009,1,31))
        request.assert_called_with(e_uri, method="GET")
