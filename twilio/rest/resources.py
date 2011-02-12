import json
import logging
import re
import urllib

from twilio.rest import core

class AvailablePhoneNumber(core.InstanceResource):
    """ An available phone number resource """

    def __init__(self, uri, entries={}, **kwargs):
        super(AvailablePhoneNumber, self).__init__(uri, entries=entries, **kwargs)

    def purchase(self, voice_url=None, voice_method=None, account_sid=None,
                 voice_fallback_url=None, voice_fallback_method=None, 
                 status_callback_method=None, sms_url=None, sms_method=None,
                 sms_fallback_url=None, sms_fallback_method=None,
                 voice_caller_id_lookup=False):
        """
        Provision the phone number and then return the new :class:`PhoneNumber` instance.
        """
        pass

class Transcription(core.InstanceResource):

    pass
    

class Transcriptions(core.ListResource):

    name = "Transcriptions"
    instance = Transcription

    def list(self):
        """
        Return a list of :class:`Transcription` resources
        """
        return self._list([])


class Recording(core.InstanceResource):

    subresources = [
        Transcriptions,
        ]
    
    def delete(self):
        """
        Delete this recording
        """
        self._delete()


class Recordings(core.ListResource):

    name = "Recordings"
    instance = Recording

    def list(self, call_sid=None, before=None, after=None):
        """
        Returns a page of :class:`Recording` resources as a list. For paging informtion see :class:`ListResource`. 

        :param date after: Only list recordings logged after this datetime
        :param date before: Only list recordings logger before this datetime
        :param call_sid: Only list recordings from this :class:`Call`
        """
        params = {
            "CallSid": call_sid,
            "DateCreated<": before,
            "DateCreated>": after,
            }
        return self._list(params)

    def delete(self, sid):
        """
        Delete the given recording
        """
        self._delete(sid)


class Notification(core.InstanceResource):

    def delete(self):
        """
        Delete this notification
        """
        self._delete()

class Notifications(core.ListResource):

    name = "Notifications"
    instance = Notification

    def list(self, before=None, after=None, log_level=None):
        """
        Returns a page of :class:`Notification` resources as a list. For paging informtion see :class:`ListResource`. 

        **NOTE**: Due to the potentially voluminous amount of data in a notification, the full HTTP request and response data is only returned in the Notification instance resource representation.
   
        :param date after: Only list notifications logged after this datetime
        :param date before: Only list notifications logger before this datetime
        :param log_level: If 1, only shows errors. If 0, only show warnings
        """
        params = core.fparam({
                "MessageDate<": before,
                "MessageDate>": after,
                "LogLevel": log_level,
                })
        return self._list(params)

    def delete(self, sid):
        """ 
        Delete a given Notificiation
        """
        self._delete(sid)

class Call(core.InstanceResource):
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

class Calls(core.ListResource):
    """ A list of Call resources """

    name = "Calls"
    instance = Call

    @core.normalize_dates
    def list(self, to=None, from_=None, status=None, ended_after=None,
             ended_before=None, ended=None, started_before=None, 
             started_after=None, started=None, page=0):
        """
        Returns a page of :class:`Call` resources as a list. For paging 
        informtion see :class:`ListResource`
   
        :param date after: Only list calls started after this datetime
        :param date before: Only list calls started before this datetime
        """
        params = core.fparam({
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
        return self._list(params)

    def create(self, to, from_, url, method=None, fallback_url=None,
             fallback_method=None, status_callback=None, status_method=None, 
             if_machine=None, send_digits=None, timeout=None):
        """
        Really just a wrapper for :meth:`create`
        """
        params = core.fparam({
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
        self._update(sid, body)

    def route(self, sid, url, method="POST"):
        """Route the specified :class:`Call` to another url.

        :param sid: A Call Sid for a specific call
        :param url: A valid URL that returns TwiML. Twilio will immediately redirect the call to the new TwiML.
        :param method: The HTTP method Twilio should use when requesting the above URL. Defaults to POST.
        :returns: Updated :class:`Call` resource
        """
        body = urllib.urlencode({"Url": url, "Method": method})
        self._update(sid, body)

class CallerId(core.InstanceResource):
    
   def delete(self):
       """
       Deletes this caller ID from the account.
       """
       self._delete(**kwargs)

   def update(self, **kwargs):
       """
       Update the CallerId
       """
       self._update(**kwargs)


class CallerIds(core.ListResource):
    """ A list of :class:`CallerId` resources """

    name = "OutgoingCallerIds"
    key = "outgoing_caller_ids"
    instance = CallerId

    def delete(self, sid):
        """
        Deletes a specific :class:`CallerId` from the account.
        """
        self._delete(sid)

    def list(self, phone_number=None, friendly_name=None):
        """
        :param phone_number: Only show the caller id resource that exactly matches this phone number.
        :param friendly_name: Only show the caller id resource that exactly  matches this name.
        """
        params = core.fparam({
            "PhoneNumber": phone_number,
            "FrienldyName": friendly_name,
            })
        return self._list(params)

    def update(self, sid, friendly_name=None):
        """
        Update a specific :class:`CallerId`
        """
        params = core.fparam({
            "FriendlyName": friendly_name,
            })
        return self._update(sid, urllib.urlencode(params))

    def validate(self, phone_number, friendly_name=None, call_delay=0, 
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
        params = core.fparam({
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

class PhoneNumber(core.InstanceResource):

   def trasfer(self, account_sid):
       """
       Transfer the phone number with sid from the current account to another identified by account_sid
       """
       pass

   def update(self, api_version=None, voice_url=None, voice_method=None, 
              voice_fallback_url=None, voice_fallback_method=None, 
              status_callback_method=None, sms_url=None, sms_method=None, 
              sms_fallback_url=None, sms_fallback_method=None, 
              voice_caller_id_lookup=False, account_sid=None):
       """
       Update this phone number instance
       """
       pass

   def delete(self):
       """
       Release this phone number from your account. Twilio will no longer answer calls to this number, and you will stop being billed the monthly phone number fees. The phone number will eventually be recycled and potentially given to another customer, so use with care. If you make a mistake, contact us... we may be able to give you the number back.
       """
       pass


class PhoneNumbers(core.ListResource):


    name ="IncomingPhoneNumbers"
    key = "incoming_phone_numbers"
    instance = PhoneNumber
    
    def delete(self, sid):
        """
        Release this phone number from your account. Twilio will no longer answer calls to this number, and you will stop being billed the monthly phone number fees. The phone number will eventually be recycled and potentially given to another customer, so use with care. If you make a mistake, contact us... we may be able to give you the number back.
        """
        return self._delete(sid)

    def list(self, phone_number=None, friendly_name=None):
        """
        :param phone_number: Only return phone numbers that match this pattern. You can specify partial numbers and use '*' as a wildcard for any digit.
        :param friendly_name: Only return phone numbers with friendly names that exactly match this name.
        """
        params = core.fparam({
               "PhoneNumber": phone_number,
               "FriendlyName": friendly_name,
               })
        return self._list(params)

    def purchase(self, phone_number=None, area_code=None, voice_url=None, 
                 voice_method=None, voice_fallback_url=None, 
                 voice_fallback_method=None, status_callback_method=None, 
                 sms_url=None, sms_method=None, sms_fallback_url=None, 
                 sms_fallback_method=None, voice_caller_id_lookup=False, 
                 account_sid=None):
        """
        Attempt to purchase the specified number. The only required parameters are **either** phone_number or area_code

        :returns: Returns a :class:`PhoneNumber` instance on success, :data:`False` on failure
        """
        pass

    def search(self, type="LOCAL", country="US", region=None, area_code=None, 
               postal_code=None, near_number=None, near_lat_long=None, lata=None,
               rate_center=None, distance=25):
        """
        :param type: Either :data:`LOCAL` or :data:`TOLL_FREE`. Defaults to :data:`LOCAL`
        :param integer area_code:
        """
        pass

    def trasfer(self, sid, account_sid):
        """
        Transfer the phone number with sid from the current account to another identified by account_sid
        """
        pass

    def update(self, sid, api_version=None, voice_url=None, voice_method=None, 
               voice_fallback_url=None, voice_fallback_method=None, 
               status_callback_method=None, sms_url=None, sms_method=None, 
               sms_fallback_url=None, sms_fallback_method=None, 
               voice_caller_id_lookup=False, account_sid=None):
        """
        Update this phone number instance
        """
        pass
       
class Sandboxes(core.ListResource):
    
    def get(self):
        """
        Return your Twilio Sandbox resource
        """
        pass

    def update(self, voice_url=None, voice_method="POST", sms_url=None, 
               sms_method="POST"):
        """
        Update your Twilio Sandbox
        """
        pass

class Sandbox(core.InstanceResource):

    def update(self, voice_url=None, voice_method="POST", sms_url=None, 
               sms_method="POST"):
        """
        Update your Twilio Sandbox
        """
        pass


class Sms(object):
    """
    Holds all the specific SMS list resources
    """

    name = "SMS"
    
    def __init__(self, client, base_uri):
        self.uri = "{0}/SMS".format(base_uri)
        self.messages = SmsMessages(client, self.uri)
    
class SmsMessage(core.InstanceResource):
    
    pass

class SmsMessages(core.ListResource):

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
        params = core.fparam({
            "To": to,
            "From": from_,
            "Body": body,
            "StatusCallback": status_callback,
            })
        return self._create(urllib.urlencode(params))

    def list(self, to=None, from_=None, before=None, after=None):
        """
        Returns a page of :class:`SMSMessage` resources as a list. For paging informtion see :class:`ListResource`. 

        :param to: Only show SMS messages to this phone number.
        :param from_: Onlye show SMS message from this phone number.
        :param date after: Only list recordings logged after this datetime
        :param date before: Only list recordings logger before this datetime
        """
        params = core.fparam({
            "To": to,
            "From": from_,
            "DateSent<": before,
            "DateSent>": after,
            })
        return self._list(params)

class Participant(core.InstanceResource):

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


class Participants(core.ListResource):

    def get(self, conference_sid, sid):
        """
        Returns a :class:`Particiapant` resource. Requires a conference sid
        
        :param conference_sid: Conference this participant is part of
        :param sid: Participant identifier
        """
        pass

    def list(conference_sid, muted=None):
        """
        Returns a list of :class:`Participant` resources in the given conference

        :param conference_sid: Conference this participant is part of
        :param boolean muted: If True, only show participants who are muted
        """
        pass

    def iter(conference_sid, muted=None):
        """
        Returns a list of :class:`Participant` resources in the given conference

        :param conference_sid: Conference this participant is part of
        :param boolean muted: If True, only show participants who are muted
        """
        pass

    def mute(self, conference_sid, participant_sid):
        """
        Mute the given participant
        """
        pass

    def unmute(self, conference_sid, participant_sid):
        """
        Unmute the given participant
        """
        pass

    def kick(self, conference_sid, participant_sid):
        """
        Remove the participant from the given conference
        """
        pass


class Conference(core.InstanceResource):

    subresources = [
        Participants
        ]
    
    pass


class Conferences(core.ListResource):

    name = "Conferences"
    instance = Conference
    
    def list(self, status=None, friendly_name=None, updated_before=None,
             updated_after=None, created_after=None, created_before=None,
             updated=None, created=None):
        """
        Return a list of :class:`Conference` resources

        :param status: Only show conferences with this status
        :param frienldy_name: Onlye show conferences with this exact frienldy_name
        :param date updated_after: Only list conferences updated after this datetime
        :param date updated_before: Only list conferences updated before this datetime
        :param date created_after: Only list conferences created after this datetime
        :param date created_before: Only list conferences created before this datetime
        """
        params = core.fparam({
            "Status": status,
            "FriendlyName": friendly_name,
            "DateUpdated<": updated_before,
            "DateUpdated>": updated_after,
            "DateUpdated": updated,
            "DateCreated<": created_before,
            "DateCreated>": created_after,
            "DateCreated": created,
            })
        return self._list(params)
    
class Account(core.InstanceResource):
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


class Accounts(core.ListResource):
    """ A list of Account resources """

    name = "Accounts"
    instance = Account

    def list(self, friendly_name=None, status=None):
        """
        Returns a page of :class:`Account` resources as a list. For paging
        informtion see :class:`ListResource`
   
        :param date after: Only list calls started after this datetime
        :param date before: Only list calls started before this datetime
        """
        params = core.fparam({
                "FriendlyName": friendly_name,
                "Status": status,
                })
        return self._list(params=params)
    
    def update(self, sid, friendly_name=None, status=None):
        """
        :param sid: Account identifier
        :param friendly_name: Update the human-readable description of this account.
        :param status: Alter the status of this account: use :data:`CLOSED` to irreversibly close this account, :data:`SUSPENDED` to temporarily suspend it, or :data:`ACTIVE` to reactivate it.
        """
        params = core.fparam({
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

