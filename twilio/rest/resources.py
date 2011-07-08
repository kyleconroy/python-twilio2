import base64
import datetime
import json
import logging
import re
import os
import urllib

from twilio import TwilioException
from twilio import TwilioRestException
from urllib import urlencode
from urlparse import urlparse

# import json
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        from django.utils import simplejson as json

# import httplib2
try:
    import httplib2
except ImportError:
    from twilio.contrib import httplib2


def transform_params(p):
    """
    Transform parameters, throwing away any None values
    and convert False and True values to strings
    """
    p = [(d,convert_boolean(p[d])) for d in p if p[d] is not None]
    return dict(p)


def parse_date(d):
    """
    Return a string representation of a date that the Twilio API understands
    Format is YYYY-MM-DD. Returns None if d is not a string, datetime, or date
    """
    if isinstance(d, datetime.datetime):
        return str(d.date())
    elif isinstance(d, datetime.date):
        return str(d)
    elif isinstance(d, str):
        return d

def convert_boolean(bool):
    if bool == True:
        return "true"
    elif bool == False:
        return "false"
    else:
        return bool


def convert_case(s):
    """
    Given a string in snake case, conver to CamelCase
    """
    return ''.join([a.title() for a in s.split("_") if a])


def convert_keys(d):
    """
    Return a dictionary with all keys converted from arguments
    """
    special = {
        "started_before": "StartTime<",
        "started_after":  "StartTime>",
        "started":        "StartTime",
        "ended_before":   "EndTime<",
        "ended_after":    "EndTime>",
        "ended":          "EndTime",
        "from_":          "From",
    }

    result = {}

    for k,v in d.iteritems():
        if k in special:
            result[special[k]] = v
        else:
            result[convert_case(k)] = v

    return result


def normalize_dates(myfunc):
    def inner_func(*args, **kwargs):
        for k, v in kwargs.iteritems():
            res = [ True for s in ["after", "before", "on"] if s in k]
            if len(res):
                kwargs[k] = parse_date(v)
        return myfunc(*args, **kwargs)
    return inner_func


class Response(object):
    """
    Take a httplib2 response and turn it into a requests response
    """

    def __init__(self, httplib_resp, content, url):
        self.content = content
        self.cached = False
        self.status_code = int(httplib_resp.status)
        self.ok = self.status_code < 400
        self.url = url


def make_request(method, url,
    params=None, data=None, headers=None, cookies=None, files=None,
    auth=None, timeout=None, allow_redirects=False, proxies=None):
    """Sends an HTTP request Returns :class:`Response <models.Response>`

    See the requests documentation for explanation of all these parameters

    Currently timeout, allow_redirects, proxies, files, and cookies
    are all ignored
    """
    http = httplib2.Http()

    if auth is not None:
        http.add_credentials(auth[0], auth[1])

    if data is not None:
        data = urlencode(data)

    if params is not None:
        enc_params = urlencode(params, doseq=True)
        if urlparse(url).query:
            url = '%s&%s' % (url, enc_params)
        else:
            url = '%s?%s' % (url, enc_params)

    resp, content = http.request(url, method, headers=headers, body=data)

    # Format httplib2 reqeusts as reqeusts objects
    return Response(resp, content, url)


def make_twilio_request(method, uri, **kwargs):
    """
    Make a request to Twilio. Throws an error
    """
    headers = kwargs.get("headers", {})
    headers["User-Agent"] = "twilio-python"   #  Add user aggent string
    headers["Accepts"] = "application/json"   #  Add accepts header

    if method == "POST" and "Content-Type" not in headers:
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    kwargs["headers"] = headers

    if "Accepts" not in headers:
        headers["Accpets"] = "application/json"
        uri = uri + ".json"

    resp = make_request(method, uri, **kwargs)

    if not resp.ok:
        try:
            error = json.loads(content)
            message = "%s: %s" % (error["code"], error["message"])
        except:
            message = content

        raise TwilioRestException(resp.status_code, resp.uri, message)

    return resp


class Resource(object):
    """A REST Resource"""

    name = "Resource"

    def __init__(self, base_uri, auth):
        self.base_uri = base_uri
        self.auth = auth

    def request(self, method, uri, **kwargs):
        """
        Send an HTTP request to the resource.

        Raise a TwilioRestException
        """
        resp = make_twilio_request(method, uri, **kwargs)
        return resp, json.loads(resp.content)

    @property
    def uri(self):
        format = (self.base_uri, self.name)
        return "%s/%s" % format


class InstanceResource(Resource):

    subresources = []

    def __init__(self, parent, sid):
        self.parent = parent
        self.name = sid
        super(InstanceResource, self).__init__(parent.uri,
            parent.auth)

    def load(self, entries):
        if "from" in entries.keys():
            entries["from_"] = entries["from"]
            del entries["from"]

        if "uri" in entries.keys():
            del entries["uri"]

        self.__dict__.update(entries)


    def load_subresources(self):
        """
        Load all subresources
        """
        for resource in self.subresources:
            list_resource = resource(self.uri, self.parent.auth)
            self.__dict__[list_resource.key] = list_resource

    def update_instance(self, **kwargs):
        a = self.parent.update(self.name, **kwargs)
        self.load(a.__dict__)

    def delete_instance(self):
        return self.parent.delete(self.name)


class ListResource(Resource):

    name = "Resources"
    instance = InstanceResource

    def __init__(self, *args, **kwargs):
        super(ListResource, self).__init__(*args, **kwargs)

        try:
            self.key
        except AttributeError:
            self.key = self.name.lower()

    def get(self, sid):
        """Return an instance resource """
        return self.get_instance(sid)

    def get_instance(self, sid):
        """Request the specified instance resource"""
        uri = "%s/%s" % (self.uri, sid)
        resp, item = self.request("GET", uri)
        return self.load_instance(item)

    def get_instances(self, params=None, page=None, page_size=None):
        """
        Query the list resource for a list of InstanceResources
        """
        params = params or {}

        if page is not None:
            params["Page"] = page

        if page_size is not None:
            params["PageSize"] = page_size

        resp, page = self.request("GET", self.uri, params=params)

        if self.key not in page:
            raise TwilioException("Key %s not present in response" % self.key)

        return [self.load_instance(ir) for ir in page[self.key]]

    def create_instance(self, body):
        """
        Create an InstanceResource via a POST to the List Resource

        :param dict body: Dictoionary of POST data
        """
        resp, instance = self.request("POST", self.uri, data=body)

        if resp.status_code != 201:
            raise TwilioRestException(resp.status,
                                      self.uri, "Resource not created")

        return self.load_instance(instance)

    def delete_instance(self, sid):
        """
        Delete an InstanceResource via DELETE

        body: string -- HTTP Body for the quest
        """
        uri = "%s/%s" % (self.uri, sid)
        resp, instance = self.request("DELETE", uri)
        return resp.status_code == 204

    def update_instance(self, sid, body):
        """
        Update an InstanceResource via a POST

        sid: string -- String identifier for the list resource
        body: string -- Dict of items to POST
        """
        uri = "%s/%s" % (self.uri, sid)
        resp, entry = self.request("POST", uri, data=body)
        return self.load_instance(entry)

    def count(self):
        """
        Return the number of instance resources contained in this list resource
        """
        resp, page =  self.request("GET", self.uri)
        return page["total"]

    def iter(self, **kwargs):
        """
        Return all instance resources using an iterator
        Can only be called on classes which implement list()

        TODO Make this use the next_url instead
        """
        p = 0
        try:
            while True:
                for r in self.list(page=p, **kwargs):
                    yield r
                p += 1
        except TwilioRestException:
            pass

    def load_instance(self, data):
        instance = self.instance(self, data["sid"])
        instance.load(data)
        instance.load_subresources()
        return instance


class AvailablePhoneNumber(InstanceResource):
    """ An available phone number resource """

    def __init__(self, list_resource, base_uri, entries):
        self.list_resource = list_resource
        self.name = ""
        self._load(entries)

    def purchase(self, **kwargs):
        return self.list_resource.purchase(phone_number=self.phone_number,
                                           **kwargs)

class AvailablePhoneNumbers(ListResource):

    name = "AvailablePhoneNumbers"
    key = "available_phone_numbers"
    instance = AvailablePhoneNumber

    types = {"LOCAL": "Local", "TOLLFREE": "TollFree"}

    def __init__(self, base_uri, auth, phone_numbers):
        super(AvailablePhoneNumbers,self).__init__(base_uri, auth)
        self.phone_numbers = phone_numbers

    def get(self, sid):
        raise TwilioException("You can't get individual available phone numbers")

    def load_instance(self, content):
        return self.instance(self.phone_numbers, self.uri, content)

    def list(self, type="LOCAL", country="US", region=None, area_code=None,
             postal_code=None, near_number=None, near_lat_long=None, lata=None,
             rate_center=None, distance=None, contains=None):
        """
        Search for phone numbers
        """
        params = transform_param({
               "InRegion": region,
               "InPostalCode": postal_code,
               "Contains": contains,
               "AreaCode": area_code,
               "InLata": lata,
               "InRateCenter": rate_center,
               "Distance": distance,
               "NearNumber": near_number,
               "NearLatLong": near_lat_long,
               })

        uri = "%s/%s/%s" % (self.uri, country, self.types[type])
        resp, page =  self.request("GET", uri, params=params)

        return [self.load_instance(i) for i in page[self.key]]


class Transcription(InstanceResource):
    pass


class Transcriptions(ListResource):

    name = "Transcriptions"
    instance = Transcription

    def list(self, **kwargs):
        """
        Return a list of :class:`Transcription` resources
        """
        return self.get_instances(**kwargs)


class Recording(InstanceResource):

    subresources = [
        Transcriptions,
        ]

    def delete(self):
        """
        Delete this recording
        """
        return self.delete_instance()


class Recordings(ListResource):

    name = "Recordings"
    instance = Recording

    @normalize_dates
    def list(self, call_sid=None, before=None, after=None, **kwargs):
        """
        Returns a page of :class:`Recording` resources as a list.
        For paging informtion see :class:`ListResource`.

        :param date after: Only list recordings logged after this datetime
        :param date before: Only list recordings logger before this datetime
        :param call_sid: Only list recordings from this :class:`Call`
        """
        params = transform_params({
            "CallSid": call_sid,
            "DateCreated<": before,
            "DateCreated>": after,
            })
        return self.get_instances(params=params)

    def delete(self, sid):
        """
        Delete the given recording
        """
        return self.delete_instance(sid)


class Notification(InstanceResource):

    def delete(self):
        """
        Delete this notification
        """
        self._delete()

class Notifications(ListResource):

    name = "Notifications"
    instance = Notification

    def list(self, before=None, after=None, log_level=None, **kwargs):
        """
        Returns a page of :class:`Notification` resources as a list. For paging informtion see :class:`ListResource`.

        **NOTE**: Due to the potentially voluminous amount of data in a notification, the full HTTP request and response data is only returned in the Notification instance resource representation.

        :param date after: Only list notifications logged after this datetime
        :param date before: Only list notifications logger before this datetime
        :param log_level: If 1, only shows errors. If 0, only show warnings
        """
        params = fparam({
                "MessageDate<": before,
                "MessageDate>": after,
                "LogLevel": log_level,
                })
        return self._list(params, **kwargs)

    def delete(self, sid):
        """
        Delete a given Notificiation
        """
        self._delete(sid)

class Call(InstanceResource):
    """ A call resource """

    BUSY        = "busy"
    CANCELED    = "canceled"
    COMPLETED   = "completed"
    FAILED      = "failed"
    IN_PROGRESS = "in-progress"
    NO_ANSWER   = "no-answer"
    QUEUED      = "queued"
    RINGING     = "ringing"

    subresources = [
        Notifications,
        Recordings,
        ]

    def hangup(self):
        """ If this call is currenlty active, hang up the call.
        If this call is scheduled to be made, remove the call
        from the queue
        """
        a = self.list_resource.hangup(self.sid)
        self._load(a.__dict__)

    def route(self, **kwargs):
        """Route the specified :class:`Call` to another url.

        :param url: A valid URL that returns TwiML. Twilio will immediately redirect the call to the new TwiML.
        :param method: The HTTP method Twilio should use when requesting the above URL. Defaults to POST.
        """
        a = self.list_resource.route(self.sid, **kwargs)
        self._load(a.__dict__)

class Calls(ListResource):
    """ A list of Call resources """

    name = "Calls"
    instance = Call

    @normalize_dates
    def list(self, to=None, from_=None, status=None, ended_after=None,
             ended_before=None, ended=None, started_before=None,
             started_after=None, started=None, **kwargs):
        """
        Returns a page of :class:`Call` resources as a list. For paging
        informtion see :class:`ListResource`

        :param date after: Only list calls started after this datetime
        :param date before: Only list calls started before this datetime
        """
        params = fparam({
            "To": to,
            "From": from_,
            "Status": status,
            "StartTime<": started_before,
            "StartTime>": started_after,
            "StartTime": started,
            "EndTime<": ended_before,
            "EndTime>": ended_after,
            "EndTime": ended,
            })
        return self._list(params, **kwargs)

    def create(self, to, from_, url, method=None, fallback_url=None,
             fallback_method=None, status_callback=None, status_method=None,
             if_machine=None, send_digits=None, timeout=None):
        """
        Really just a wrapper for :meth:`create`
        """
        params = fparam({
            "To": to,
            "From": from_,
            "Url": url,
            "Method": method,
            "FallbackUrl": fallback_url,
            "FallbackMethod": fallback_method,
            "StatusCallback": status_callback,
            "StatusCallbackMethod": status_method,
            "SendDigits": send_digits,
            "Timeout": timeout,
            "IfMachine": if_machine,
            })
        return self._create(urllib.urlencode(params))

    def hangup(self, sid):
        """ If this call is currenlty active, hang up the call.
        If this call is scheduled to be made, remove the call
        from the queue

        :param sid: A Call Sid for a specific call
        :returns: Updated :class:`Call` resource
        """
        body = urllib.urlencode({"Status": Call.CANCELED})
        return self._update(sid, body)

    def route(self, sid, url, method="POST"):
        """Route the specified :class:`Call` to another url.

        :param sid: A Call Sid for a specific call
        :param url: A valid URL that returns TwiML. Twilio will immediately redirect the call to the new TwiML.
        :param method: The HTTP method Twilio should use when requesting the above URL. Defaults to POST.
        :returns: Updated :class:`Call` resource
        """
        body = urllib.urlencode({"Url": url, "Method": method})
        return self._update(sid, body)

class CallerId(InstanceResource):

   def delete(self):
       """
       Deletes this caller ID from the account.
       """
       self._delete()

   def update(self, **kwargs):
       """
       Update the CallerId
       """
       self._update(**kwargs)


class CallerIds(ListResource):
    """ A list of :class:`CallerId` resources """

    name = "OutgoingCallerIds"
    key = "outgoing_caller_ids"
    instance = CallerId

    def delete(self, sid):
        """
        Deletes a specific :class:`CallerId` from the account.
        """
        self._delete(sid)

    def list(self, phone_number=None, friendly_name=None, **kwargs):
        """
        :param phone_number: Only show the caller id resource that exactly matches this phone number.
        :param friendly_name: Only show the caller id resource that exactly  matches this name.
        """
        params = fparam({
            "PhoneNumber": phone_number,
            "FrienldyName": friendly_name,
            })
        return self._list(params, **kwargs)

    def update(self, sid, friendly_name=None):
        """
        Update a specific :class:`CallerId`
        """
        params = fparam({
            "FriendlyName": friendly_name,
            })
        return self._update(sid, urllib.urlencode(params))

    def validate(self, phone_number, friendly_name=None, call_delay=None,
                 extension=None):
        """
        Begin the validation procress for the given number.

        Returns a dictionary with the following keys

        * **account_sid**: The unique id of the Account to which the Validation Request belongs.
        * **phone_number**: The incoming phone number being validated, formatted with a '+' and country code e.g., +16175551212 (E.164 format).
        * **friendly_name**: The friendly name you provided, if any.
        * **validation_code**: The 6 digit validation code that must be entered via the phone to validate this phone number for Caller ID.

        :param phone_number: The phone number to call and validate
        :param friendly_name: A human readable description for the new caller ID with maximum length 64 characters. Defaults to a nicely formatted version of the number.
        :param call_delay: The number of seconds, between 0 and 60, to delay before initiating the validation call.
        :param extension: Digits to dial after connecting the validation call.
        :returns: A response dictionary
        """
        params = fparam({
                "PhoneNumber": phone_number,
                "FriendlyName": friendly_name,
                "CallDelay": call_delay,
                "Extension": extension,
                })

        hs = {'Content-type': 'application/x-www-form-urlencoded'}
        body = urllib.urlencode(params)
        resp, content =  self._request(self.uri, method="POST", body=body,
                                       headers=hs)
        return json.loads(content)

class PhoneNumber(InstanceResource):

    def trasfer(self, account_sid):
        """
        Transfer the phone number with sid from the current account to another identified by account_sid
        """
        pass

    def update(self, **kwargs):
        """
        Update this phone number instance
        """
        a = self.list_resource.update(self.sid, **kwargs)
        self._load(a.__dict__)

    def delete(self):
        """
        Release this phone number from your account. Twilio will no longer answer calls to this number, and you will stop being billed the monthly phone number fees. The phone number will eventually be recycled and potentially given to another customer, so use with care. If you make a mistake, contact us... we may be able to give you the number back.
        """
        a = self.list_resource.delete(self.sid)


class PhoneNumbers(ListResource):


    name ="IncomingPhoneNumbers"
    key = "incoming_phone_numbers"
    instance = PhoneNumber

    def __init__(self, client, base_uri):
        super(PhoneNumbers,self).__init__(client, base_uri)
        self.available_phone_numbers = AvailablePhoneNumbers(client, base_uri, self)

    def delete(self, sid):
        """
        Release this phone number from your account. Twilio will no longer answer calls to this number, and you will stop being billed the monthly phone number fees. The phone number will eventually be recycled and potentially given to another customer, so use with care. If you make a mistake, contact us... we may be able to give you the number back.
        """
        return self._delete(sid)

    def list(self, phone_number=None, friendly_name=None, **kwargs):
        """
        :param phone_number: Only return phone numbers that match this pattern. You can specify partial numbers and use '*' as a wildcard for any digit.
        :param friendly_name: Only return phone numbers with friendly names that exactly match this name.
        """
        params = fparam({
               "PhoneNumber": phone_number,
               "FriendlyName": friendly_name,
               })
        return self._list(params, **kwargs)

    def purchase(self, phone_number=None, area_code=None, voice_url=None,
                 voice_method=None, voice_fallback_url=None,
                 voice_fallback_method=None, status_callback_method=None,
                 sms_url=None, sms_method=None, sms_fallback_url=None,
                 sms_fallback_method=None, voice_caller_id_lookup=None,
                 account_sid=None):
        """
        Attempt to purchase the specified number. The only required parameters are **either** phone_number or area_code

        :returns: Returns a :class:`PhoneNumber` instance on success, :data:`False` on failure
        """
        params = fparam({
                "VoiceUrl": voice_url,
                "VoiceMethod": voice_method,
                "VoiceFallbackUrl": voice_fallback_url,
                "VoiceFallbackMethod": voice_fallback_method,
                "SmsUrl": sms_url,
                "SmsMethod": sms_method,
                "SmsFallbackUrl": sms_fallback_url,
                "SmsFallbackMethod": sms_fallback_method,
                "VoiceCallerIdLookup": voice_caller_id_lookup,
                "AccountSid": account_sid,
               })

        if phone_number:
            params["PhoneNumber"] = phone_number
        elif area_code:
            params["AreaCode"] = area_code
        else:
            raise TypeError("phone_number or area_code is required")

        return self._create(urllib.urlencode(params))

    def search(self, **kwargs):
        """
        :param type: The type of phone number to search for. Either :data:`LOCAL` or :data:`TOLL_FREE`. Defaults to :data:`LOCAL`
        :param integer country: Either :data:`US` or :data:`CA`. Defaults to :data:`US`
        :param string region: If searching the US, only show numbers in this state
        :param string postal_code: Only show numbers in this area code
        :param string rate_center: US only.
        :param tuple near_lat_long: Given a latitude/longitude tupe (lat,long) find geographically close numbers within Distance miles.
        :param integer distance: Specifies the search radius for a Near- query in miles. Defaults to 25 miles.
        """
        return self.available_phone_numbers.list(**kwargs)

    def trasfer(self, sid, account_sid):
        """
        Transfer the phone number with sid from the current account to another identified by account_sid
        """
        body = urllib.urlencode({"Url": url, "Method": method})
        return self._update(sid, body)

    def update(self, sid, api_version=None, voice_url=None, voice_method=None,
               voice_fallback_url=None, voice_fallback_method=None,
               status_callback_method=None, sms_url=None, sms_method=None,
               sms_fallback_url=None, sms_fallback_method=None,
               voice_caller_id_lookup=None, account_sid=None):
        """
        Update this phone number instance
        """
        params = fparam({
                "ApiVersion": api_version,
                "VoiceUrl": voice_url,
                "VoiceMethod": voice_method,
                "VoiceFallbackUrl": voice_fallback_url,
                "VoiceFallbackMethod": voice_fallback_method,
                "StatusCallbackMethod": status_callback_method,
                "SmsUrl": sms_url,
                "SmsMethod": sms_method,
                "SmsFallbackUrl": sms_fallback_url,
                "SmsFallbackMethod": sms_fallback_method,
                "VoiceCallerIdLookup": voice_caller_id_lookup,
                "AccountSid": account_sid,
                })
        return self._update(sid, urllib.urlencode(params))

class Sandbox(InstanceResource):

    id_key = "pin"

    def update(self, **kwargs):
        """
        Update your Twilio Sandbox
        """
        a = self.list_resource.update(**kwargs)
        self._load(a.__dict__)


class Sandboxes(ListResource):

    name = "Sandbox"
    instance = Sandbox

    def get(self):
        """Request the specified instance resource"""
        return self._get(self.uri)

    def update(self, voice_url=None, voice_method=None, sms_url=None,
               sms_method=None):
        """
        Update your Twilio Sandbox
        """
        body = urllib.urlencode(fparam({
                "VoiceUrl": voice_url,
                "VoiceMethod": voice_method,
                "SmsUrl": sms_url,
                "SmsMethod": sms_method,
                }))
        hs = {'Content-type': 'application/x-www-form-urlencoded'}
        resp, content =  self._request(self.uri, method="POST", body=body,
                                       headers=hs)
        entries = json.loads(content)
        return self._create_instance(entries)


class Sms(object):
    """
    Holds all the specific SMS list resources
    """

    name = "SMS"
    key = "sms"

    def __init__(self, client, base_uri):
        self.uri = "%s/SMS" % (base_uri)
        self.messages = SmsMessages(client, self.uri)

class SmsMessage(InstanceResource):

    pass

class SmsMessages(ListResource):

    name = "Messages"
    key = "sms_messages"
    instance = SmsMessage

    def create(self, to=None, from_=None, body=None, status_callback=None):
        """
        Create and send a SMS Message.

        :param to: **Required** - The destination phone number.
        :param from_: **Required** - Only show SMS message from this phone number.
        :param body: **Required** - The text of the message you want to send, limited to 160 characters.
        :param status_callback: A URL that Twilio will POST to when your message is processed. Twilio will POST the SmsSid as well as SmsStatus=sent or SmsStatus=failed.
        """
        params = fparam({
            "To": to,
            "From": from_,
            "Body": body,
            "StatusCallback": status_callback,
            })
        return self._create(urllib.urlencode(params))

    def list(self, to=None, from_=None, before=None, after=None, **kwargs):
        """
        Returns a page of :class:`SMSMessage` resources as a list. For paging informtion see :class:`ListResource`.

        :param to: Only show SMS messages to this phone number.
        :param from_: Onlye show SMS message from this phone number.
        :param date after: Only list recordings logged after this datetime
        :param date before: Only list recordings logger before this datetime
        """
        params = fparam({
            "To": to,
            "From": from_,
            "DateSent<": before,
            "DateSent>": after,
            })
        return self._list(params, **kwargs)

class Participant(InstanceResource):

    id_key = "call_sid"

    def mute(self):
        """
        Mute the participant
        """
        self._update(muted="true")

    def unmute(self):
        """
        Unmute the participant
        """
        self._update(muted="false")

    def kick(self):
        """
        Remove the participant from the given conference
        """
        self._delete()


class Participants(ListResource):

    name = "Participants"
    instance = Participant

    def list(self, muted=None, **kwargs):
        """
        Returns a list of :class:`Participant` resources in the given conference

        :param conference_sid: Conference this participant is part of
        :param boolean muted: If True, only show participants who are muted
        """
        params = fparam({
            "Muted": muted,
            })
        return self._list(params, **kwargs)

    def mute(self, call_sid):
        """
        Mute the given participant
        """
        return self.update(call_sid, muted=True)

    def unmute(self, call_sid):
        """
        Unmute the given participant
        """
        return self.update(call_sid, muted=False)

    def kick(self, call_sid):
        """
        Remove the participant from the given conference
        """
        return self._delete(call_sid)

    def delete(self, call_sid):
        """
        Remove the participant from the given conference
        """
        return self._delete(call_sid)

    def update(self, sid, muted=None):
        """
        :param sid: Account identifier
        :param friendly_name: Update the human-readable description of this account.
        :param status: Alter the status of this account: use :data:`CLOSED` to irreversibly close this account, :data:`SUSPENDED` to temporarily suspend it, or :data:`ACTIVE` to reactivate it.
        """
        params = fparam({
                "Muted": muted
                })
        return self._update(sid, urllib.urlencode(params))


class Conference(InstanceResource):

    subresources = [
        Participants
        ]


class Conferences(ListResource):

    name = "Conferences"
    instance = Conference

    def list(self, status=None, friendly_name=None, updated_before=None,
             updated_after=None, created_after=None, created_before=None,
             updated=None, created=None, **kwargs):
        """
        Return a list of :class:`Conference` resources

        :param status: Only show conferences with this status
        :param frienldy_name: Onlye show conferences with this exact frienldy_name
        :param date updated_after: Only list conferences updated after this datetime
        :param date updated_before: Only list conferences updated before this datetime
        :param date created_after: Only list conferences created after this datetime
        :param date created_before: Only list conferences created before this datetime
        """
        params = fparam({
            "Status": status,
            "FriendlyName": friendly_name,
            "DateUpdated<": updated_before,
            "DateUpdated>": updated_after,
            "DateUpdated": updated,
            "DateCreated<": created_before,
            "DateCreated>": created_after,
            "DateCreated": created,
            })
        return self._list(params, **kwargs)

class Account(InstanceResource):
    """ An Account resource """

    ACTIVE    = "active"
    SUSPENDED = "suspended"
    CLOSED    = "closed"

    subresources = [
        Notifications,
        Transcriptions,
        Recordings,
        Calls,
        Sms,
        CallerIds,
        PhoneNumbers,
        Conferences,
        ]

    def update(self, **kwargs):
        """
        :param friendly_name: Update the human-readable description of this account.
        :param status: Alter the status of this account: use :data:`CLOSED` to irreversibly close this account, :data:`SUSPENDED` to temporarily suspend it, or :data:`ACTIVE` to reactivate it.
        """
        self._update(**kwargs)

    def close(self):
         """
         Permenently deactivate an account, Alias to update
         """
         return self._update(status=Account.CLOSED)

    def suspend(self):
        """
        Temporarily suspend an account, Alias to update
        """
        return self._update(status=Account.SUSPENDED)

    def activate(self):
        """
        Reactivate an account, Alias to update
        """
        return self._update(status=Account.ACTIVE)


class Accounts(ListResource):
    """ A list of Account resources """

    name = "Accounts"
    instance = Account

    def list(self, friendly_name=None, status=None, **kwargs):
        """
        Returns a page of :class:`Account` resources as a list. For paging
        informtion see :class:`ListResource`

        :param date after: Only list calls started after this datetime
        :param date before: Only list calls started before this datetime
        """
        params = fparam({
                "FriendlyName": friendly_name,
                "Status": status,
                })
        return self._list(params, **kwargs)

    def update(self, sid, friendly_name=None, status=None):
        """
        :param sid: Account identifier
        :param friendly_name: Update the human-readable description of this account.
        :param status: Alter the status of this account: use :data:`CLOSED` to irreversibly close this account, :data:`SUSPENDED` to temporarily suspend it, or :data:`ACTIVE` to reactivate it.
        """
        params = fparam({
                "FriendlyName": friendly_name,
                "Status": status
                })
        return self._update(sid, urllib.urlencode(params))

    def close(self, sid):
        """
        Permenently deactivate an account, Alias to update
        """
        return self.update(sid, status=Account.CLOSED)

    def suspend(self, sid):
        """
        Temporarily suspend an account, Alias to update
        """
        return self.update(sid, status=Account.SUSPENDED)

    def activate(self, sid):
        """
        Reactivate an account, Alias to update
        """
        return self.update(sid, status=Account.ACTIVE)

    def create(self, friendly_name):
        """
        Returns a newly created sub account resource.

        :param friendly_name: Update the human-readable description of this account.
        """
        body = urllib.urlencode({ "FriendlyName":friendly_name })
        return self._create(body)

