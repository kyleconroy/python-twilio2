import httplib2
import logging
from twilio.rest.core import Client
from twilio.rest.resources import *
from urllib import urlencode 
from urlparse import urljoin

class Twilio(Client):
    """
    Http Client wrapper class, so we can 
    use whatever underlying http client
    """
    
    def __init__(self, account=None, token=None, base="https://api.twilio.com",
                 version="2010-04-01"):
        uri = "/%s/Accounts/%s" % (version, account)

        # self.accounts                = Accounts(uri, client=self)
        self.available_phone_numbers = AvailablePhoneNumbers(uri, client=self)
        self.calls                   = Calls(uri, client=self)
        # self.conferences             = Conferences(uri, client=self)
        # self.groups                  = Groups(uri, client=self)
        # self.incoming_phone_numbers  = IncomingPhoneNumbers(uri, client=self)
        # self.notifications           = Notifications(uri, client=self)
        self.outgoing_caller_ids     = OutgoingCallerIds(uri, client=self)
        # self.recordings              = Recordings(uri, client=self)
        # self.sms_messages            = Messages(uri, client=self)
        # self.transcriptions          = Transcriptions(uri, client=self)

        super(Twilio, self).__init__(account, token, base=base)
