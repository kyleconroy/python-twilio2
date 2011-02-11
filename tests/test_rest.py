import json
import os
import unittest

from mock import patch
from mock import Mock
from twilio.rest.resources import *
from twilio.rest.client import TwilioClient
from twilio.rest.core import TwilioException

ACCOUNT_SID = "AC111111111"
AUTH_TOKEN = "AUTH_TOKEN"
BASE_URI = "https://api.twilio.com/2010-04-01/"

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
        request = Mock()
        request.return_value = 4,5
        self.mock_http.request = request

        self.c.accounts.create(friendly_name="MyNewAccount")

        uri = "{0}.json".format(self.c.accounts.uri)
        body = "FriendlyName=MyNewAccount"
        request.assert_called_with(uri, method="POST", body=body)

    def test_instance_creation(self):

        with open("tests/http/create_account_content.json") as f:
            content = f.read()

        entries = json.loads(content)

        print self.c.accounts.instance
        a = self.c.accounts._create_instance(content)

        self.assertEquals(a.sid, entries["sid"])

class ResourceTest(unittest.TestCase):

    def test_resource(self):
        pass
