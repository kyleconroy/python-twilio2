import logging
import os

from twilio import TwilioException
from twilio.rest.resources import Accounts
from twilio.rest.resources import Calls
from urllib import urlencode
from urlparse import urljoin


def find_credentials(self):
    """
    Look in the current environment for Twilio credentails
    """
    try:
        account = os.environ["TWILIO_ACCOUNT_SID"]
        token   = os.environ["TWILIO_AUTH_TOKEN"]
        return account, token
    except KeyError:
        return None, None


class TwilioRestClient(object):
    """
    A client for accessing the Twilio REST API
    """

    def request(self, *args, **kwargs):
        return self.client.request(*args, **kwargs)

    def __init__(self, account=None, token=None, base="https://api.twilio.com",
                 version="2010-04-01", client=None):
        """
        Create a Twilio REST API client.
        """

        # Get account credentials
        if not account or not token:
            account, token = find_credentials()
            if not account or not token:
                raise TwilioException("Could not find account credentials")

        self.account_sid = account
        self.auth_token = token

        # Make Client
        self.client = client or httplib2.Http()
        self.client.add_credentials(account, token)

        version_uri = "%s/%s" % (base, version)
        account_uri = "%s/%s/Accounts/%s" % (base, version, account)

        self.accounts       = Accounts(self.client, version_uri)
        self.calls          = Calls(self.client, account_uri)
        self.caller_ids     = CallerIds(self.client, account_uri)
        self.notifications  = Notifications(self.client, account_uri)
        self.recordings     = Recordings(self.client, account_uri)
        self.transcriptions = Transcriptions(self.client, account_uri)
        self.sms            = Sms(self.client, account_uri)
        self.phone_numbers  = PhoneNumbers(self.client, account_uri)
        self.conferences    = Conferences(self.client, account_uri)
        self.sandboxes      = Sandboxes(self.client, account_uri)
