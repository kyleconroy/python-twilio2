import logging
import os

from twilio.rest.core import TwilioException
from twilio.rest.resources import *
from urllib import urlencode 
from urlparse import urljoin

# import json
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json

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

    def __init__(self, account=None, token=None, base="https://api.twilio.com",
                 version="2010-04-01"):


        # Get account credentials
        if not account and not token:
            account, token = self._credentials_lookup()
            if not account and not token:
                raise TwilioException("Could not find account credentials")

        self.account_sid = account
        self.auth_token = token

        version_uri = "/{0}/".format(version)
        account_uri = "/{0}/Accounts/{1}/".format(version, account)

        self.accounts       = Accounts(version_uri, client=self)
        # self.phone_numbers  = AvailablePhoneNumbers(uri, client=self)
        # self.calls          = Calls(uri, client=self)
        # self.conferences    = Conferences(uri, client=self)
        # self.notifications  = Notifications(uri, client=self)
        # self.caller_ids     = OutgoingCallerIds(uri, client=self)
        # self.recordings     = Recordings(uri, client=self)
        # self.sms            = Sms(uri, client=self)
        # self.transcriptions = Transcriptions(uri, client=self)
        # self.groups       = Groups(uri, client=self)
