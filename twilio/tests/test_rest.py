import unittest
import os

from mock import patch
from twilio.rest.resources import *
from twilio.rest.client import TwilioClient
from twilio.rest.core import TwilioException

class ClientTest(unittest.TestCase):

    def setUp(self):
        self.ACCOUNT_SID = "AC111111111"
        self.AUTH_TOKEN = "AUTH_TOKEN"

    def test_creation(self):
        c = TwilioClient(account=self.ACCOUNT_SID, token=self.AUTH_TOKEN)
        self.assertEquals(c.account_sid, self.ACCOUNT_SID)
        self.assertEquals(c.auth_token, self.AUTH_TOKEN)

    def test_creation_env_variables(self):
        creds = {
            "TWILIO_ACCOUNT_SID": self.ACCOUNT_SID,
            "TWILIO_AUTH_TOKEN": self.AUTH_TOKEN,
            }
        
        with patch.dict(os.environ, creds):
            c = TwilioClient()

        self.assertEquals(c.account_sid, self.ACCOUNT_SID)
        self.assertEquals(c.auth_token, self.AUTH_TOKEN)

    def test_creation_fails(self):
        with self.assertRaises(TwilioException) as cm:
            c = TwilioClient()

class ResourceTest(unittest.TestCase):

    def test_resource(self):
        pass
