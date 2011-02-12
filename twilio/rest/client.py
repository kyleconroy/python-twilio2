import logging
import os

from twilio.rest.core import TwilioException
from twilio.rest.resources import *
from urllib import urlencode 
from urlparse import urljoin

# import httplib2
try:
    import httplib2
except ImportError:
    from twilio.contrib import httplib2

class TwilioClient(object):
    """
    
    """

    def _credentials_lookup(self):
        try:
            account = os.environ["TWILIO_ACCOUNT_SID"]
            token   = os.environ["TWILIO_AUTH_TOKEN"]
            return account, token
        except KeyError:
            return None, None

    def request(self, *args, **kwargs):
        return self.client.request(*args, **kwargs)

    def __init__(self, account=None, token=None, base="https://api.twilio.com",
                 version="2010-04-01", client=None):

        # Get account credentials
        if not account or not token:
            account, token = self._credentials_lookup()
            if not account or not token:
                raise TwilioException("Could not find account credentials")

        self.account_sid = account
        self.auth_token = token
        
        # Make Client
        self.client = client or httplib2.Http()
        self.client.add_credentials(account, token)

        version_uri = "{0}/{1}".format(base, version)
        account_uri = "{0}/{1}/Accounts/{2}".format(base, version, account)

        self.accounts       = Accounts(self.client, version_uri)
        self.calls          = Calls(self.client, account_uri)
        self.caller_ids     = CallerIds(self.client, account_uri)
        # self.phone_numbers  = AvailablePhoneNumbers(uri, client=self)
        # self.conferences    = Conferences(uri, client=self)
        # self.notifications  = Notifications(uri, client=self)
        # self.recordings     = Recordings(uri, client=self)
        # self.sms            = Sms(uri, client=self)
        # self.transcriptions = Transcriptions(uri, client=self)
        # self.groups       = Groups(uri, client=self)
