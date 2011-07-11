import unittest
from twilio.util import TwilioValidation


class ValidationTest(unittest.TestCase):

    def test_validation(self):
        sid = "AC9a9f9392lad99kla0sklakjs90j092j3"
        token = "1c892n40nd03kdnc0112slzkl3091j20"
        validator = TwilioValidation(sid, token)

        uri = "http://www.postbin.org/1ed898x"
        params = {
            "AccountSid": "AC9a9f9392lad99kla0sklakjs90j092j3",
            "ApiVersion": "2010-04-01",
            "CallSid": "CAd800bb12c0426a7ea4230e492fef2a4f",
            "CallStatus": "ringing",
            "Called": "+15306384866",
            "CalledCity": "OAKLAND",
            "CalledCountry": "US",
            "CalledState": "CA",
            "CalledZip": "94612",
            "Caller": "+15306666666",
            "CallerCity": "SOUTH LAKE TAHOE",
            "CallerCountry": "US",
            "CallerName": "CA Wireless Call",
            "CallerState": "CA",
            "CallerZip": "89449",
            "Direction": "inbound",
            "From": "+15306666666",
            "FromCity": "SOUTH LAKE TAHOE",
            "FromCountry": "US",
            "FromState": "CA",
            "FromZip": "89449",
            "To": "+15306384866",
            "ToCity": "OAKLAND",
            "ToCountry": "US",
            "ToState": "CA",
            "ToZip": "94612",
            }

        expected = "fF+xx6dTinOaCdZ0aIeNkHr/ZAA="
        sig = validator.sign(uri, params)

        self.assertEquals(sig, expected)
        self.assertTrue(validator.validate(uri, params, expected))
