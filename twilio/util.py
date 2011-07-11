import base64
import hmac
from hashlib import sha1


class TwilioValidation(object):

    def __init__(self, id, token):
        """Initialize a twilio utility object

        Arguments:
        id     -- Twilio Account SID
        token  -- Twilio Auth Token

        Returns a Twilio util object
        """
        self.id = id
        self.token = token

    def sign(self, uri, params):
        """Compute the signature for a given request

        uri       -- the full URI that Twilio requested on your server
        params    -- post vars that Twilio sent with the request

        Returns the computed signature
        """
        s = uri
        if len(params) > 0:
            for k, v in sorted(params.items()):
                s += k + v

        # compute signature and compare signatures
        computed = base64.encodestring(hmac.new(self.token, s, sha1).digest())
        return computed.strip()

    def validate(self, uri, params, signature):
        """Validate a request from Twilio

        uri       -- the full URI that Twilio requested on your server
        params    -- post vars that Twilio sent with the request
        signature -- signature in HTTP X-Twilio-Signature header

        returns true if the request passes validation, false if not
        """
        return self.sign(uri, params) == signature
