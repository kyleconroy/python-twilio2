from twilio.api.client import Twilio
import keys
import logging
import xml.dom.minidom
import json

logging.basicConfig(level=logging.DEBUG)

ACCOUNT_SID = keys.LOCAL["sid"]
AUTH_TOKEN = keys.LOCAL["token"]
BASE = keys.LOCAL["base"]

twilio = Twilio(ACCOUNT_SID, AUTH_TOKEN, base=BASE)

def print_sample_code(uri):
    xml_uri = uri + ".xml"
    json_uri = uri + ".json"

    xml_s = twilio.request(xml_uri, "GET")
    json_s = twilio.request(json_uri, "GET")
    
    print xml_s

    print json_s


# Outgoing Caller Ids
uri = twilio.calls.uri + "/CAc7a1fe47b14637f42fd94274d1907a1d"

print twilio.request("/2010-04-01/Accounts/foo.xml", "GET")





