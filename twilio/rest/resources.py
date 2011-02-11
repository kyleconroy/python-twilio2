import json
import logging
import re
import urllib

from twilio.rest import core

class OutgoingCallerIds(core.ListResource):
    """ A list of CallerId resources """

    def __init__(self, uri, **kwargs):
        name = "outgoing_caller_ids"
        uri += "/OutgoingCallerIds"
        super(OutgoingCallerIds, self).__init__(uri, name=name, **kwargs)

    def _load_instance(self, d):
        return OutgoingCallerId(self.uri, client=self.client, entries=d)

class OutgoingCallerId(core.InstanceResource):
    """ A Form resource """

    def __init__(self, uri, entries={}, **kwargs):
        if "sid" not in entries:
            raise core.TwilioException, "OutgoingCallerId sid missing"
        uri += "/" + entries["sid"]

        super(OutgoingCallerId, self).__init__(uri, entries=entries, **kwargs)


class AvailablePhoneNumbers(core.ListResource):
    """ A list of CallerId resources """

    def __init__(self, uri, **kwargs):
        name = "available_phone_numbers"
        uri += "/AvailablePhoneNumbers"
        super(AvailablePhoneNumbers, self).__init__(uri, name=name, **kwargs)

    def _load_instance(self, d):
        return AvailablePhoneNumber(self.uri, client=self.client, entries=d)

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

class Account(core.InstanceResource):
    """ An Account resource """

    ACTIVE    = "active"
    SUSPENDED = "suspended"
    CLOSED    = "closed"

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

    def create(self, friendly_name=None):
        """
        Returns a newly created sub account resource.
        
        :param friendly_name: Update the human-readable description of this account.
        """
        if not friendly_name:
            raise TypeError("friendly_name argument required")

        body = urllib.urlencode({ "FriendlyName":friendly_name })
        return self._create(body)

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

    def hangup(self):
        """ If this call is currenlty active, hang up the call. 
        If this call is scheduled to be made, remove the call
        from the queue
        """
        pass

    def route(self, url, method="POST"):
        """Route the specified :class:`Call` to another url.

        :param url: A valid URL that returns TwiML. Twilio will immediately redirect the call to the new TwiML.
        :param method: The HTTP method Twilio should use when requesting the above URL. Defaults to POST.
        """
        pass


class Calls(core.ListResource):
    """ A list of Call resources """

    name = "Calls"
    instance = Call

    @core.normalize_dates
    def list(self, **kwargs):
        """
        Returns a page of :class:`Call` resources as a list. For paging 
        informtion see :class:`ListResource`

        Options Arguments:
        * to
        * from_
        * status
        * ended_after
        * ended_before
        * ended
        * started_before 
        * started_after
        * started
        * page
        """
        # opt_args = ["to", "from_", "status", "ended_after", "ended_before", "ended"      * started_before 
        # * started_after
        # * started
        # * page
        # for k, v in kwargs.iteritems():
        #     if k not in opt_args:
        #         raise TypeError("list() got an unexpected keyword argument '{0}'".format(k))
        return self._list(core.convert_keys(kwargs))

    @core.normalize_dates
    def iter(self, to=None, from_=None, status=None, 
             before=None, after=None, page=0):
        """
        Returns a iterator of **all** :class:`Call` resources. 
   
        :param date after: Only list calls started after this datetime
        :param date before: Only list calls started before this datetime
        """
        pass

    def make(self, to, from_, url=None, method=None, fallback_url=None,
             fallback_method=None, status_callback=None, status_method=None, 
             if_machine=None, timeout=60):
        """
        Really just a wrapper for :meth:`create`
        """
        pass

    def hangup(self, sid):
        """ If this call is currenlty active, hang up the call. 
        If this call is scheduled to be made, remove the call
        from the queue

        :param sid: A Call Sid for a specific call
        :returns: Updated :class:`Call` resource
        """
        pass

    def route(self, sid, url, method="POST"):
        """Route the specified :class:`Call` to another url.

        :param sid: A Call Sid for a specific call
        :param url: A valid URL that returns TwiML. Twilio will immediately redirect the call to the new TwiML.
        :param method: The HTTP method Twilio should use when requesting the above URL. Defaults to POST.
        :returns: Updated :class:`Call` resource
        """
        pass


class CallerIds(core.ListResource):
    """ A list of :class:`CallerId` resources """
    
    def delete(self, sid):
        """
        Deletes a specific :class:`CallerId` from the account.
        """
        pass

    def list(self, phone_number=None, friendly_name=None):
        """
        :param phone_number: Only show the caller id resource that exactly matches this phone number.
        :param friendly_name: Only show the caller id resource that exactly  matches this name.
        """
        pass

    def iter(self, phone_number=None, friendly_name=None):
        """
        :param phone_number: Only show the caller id resource that exactly matches this phone number.
        :param friendly_name: Only show the caller id resource that exactly matches this name.
        """
        pass

    def update(self, sid, friendly_name=None):
        """
        Update a specific :class:`CallerId`
        """
        pass

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
        pass

class CallerId(core.InstanceResource):
    
   def delete(self):
       """
       Deletes this caller ID from the account.
       """
       pass

   def update(self, friendly_name=None):
       """
       Update the CallerId
       """
       pass

class Notifications(core.ListResource):

    def list(self, before=None, after=None, log_level=None):
        """
        Returns a page of :class:`Notification` resources as a list. For paging informtion see :class:`ListResource`. 

        **NOTE**: Due to the potentially voluminous amount of data in a notification, the full HTTP request and response data is only returned in the Notification instance resource representation.
   
        :param date after: Only list notifications logged after this datetime
        :param date before: Only list notifications logger before this datetime
        :param log_level: If 1, only shows errors. If 0, only show warnings
        """
        pass

    def iter(self, before=None, after=None, log_level=None):
        """
        Returns a iterator of **all** :class:`Notification` resources as a list. For paging informtion see :class:`ListResource`. 

        **NOTE**: Due to the potentially voluminous amount of data in a notification, the full HTTP request and response data is only returned in the Notification instance resource representation.
   
        :param date after: Only list notifications logged after this datetime
        :param date before: Only list notifications logger before this datetime
        :param log_level: If 1, only shows errors. If 0, only show warnings
        """
        pass

    def delete(self, sid):
        """ 
        Delete a given Notificiation
        """
        pass

class Notification(core.InstanceResource):

    def delete(self):
        """
        Delete this notification
        """
        pass

class PhoneNumbers(core.ListResource):

   def delete(self, sid):
       """
       Release this phone number from your account. Twilio will no longer answer calls to this number, and you will stop being billed the monthly phone number fees. The phone number will eventually be recycled and potentially given to another customer, so use with care. If you make a mistake, contact us... we may be able to give you the number back.
       """
       pass

   def list(self, phone_number=None, friendly_name=None):
       """
       :param phone_number: Only return phone numbers that match this pattern. You can specify partial numbers and use '*' as a wildcard for any digit.
       :param friendly_name: Only return phone numbers with friendly names that exactly match this name.
       """
       pass

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

class Recordings(core.ListResource):

    def list(self, call_sid=None, before=None, after=None):
        """
        Returns a page of :class:`Recording` resources as a list. For paging informtion see :class:`ListResource`. 

        :param date after: Only list recordings logged after this datetime
        :param date before: Only list recordings logger before this datetime
        :param call_sid: Only list recordings from this :class:`Call`
        """
        pass

    def iter(self, call_sid=None, before=None, after=None):
        """
        Returns a page of :class:`Recording` resources as a list. For paging informtion see :class:`ListResource`. 

        :param date after: Only list recordings logged after this datetime
        :param date before: Only list recordings logger before this datetime
        :param call_sid: Only list recordings from this :class:`Call`
        """
        pass

    def delete(self, sid):
        """
        Delete the given recording
        """
        pass

class Recording(core.InstanceResource):
    
    def delete(self):
        """
        Delete this recording
        """
        pass

class Sms(object):
    """
    Holds all the specific SMS list resources
    """
    def __init__(self):
        self.messages = []
    
class SmsMessages(core.ListResource):

    def create(self, to=None, from_=None, body=None, status_callback=None):
        """
        Create and send a SMS Message.

        :param to: **Required** - The destination phone number.
        :param from_: **Required** - Only show SMS message from this phone number.
        :param body: **Required** - The text of the message you want to send, limited to 160 characters.
        :param status_callback: A URL that Twilio will POST to when your message is processed. Twilio will POST the SmsSid as well as SmsStatus=sent or SmsStatus=failed.
        """
        pass

    def list(self, to=None, from_=None, before=None, after=None):
        """
        Returns a page of :class:`SMSMessage` resources as a list. For paging informtion see :class:`ListResource`. 

        :param to: Only show SMS messages to this phone number.
        :param from_: Onlye show SMS message from this phone number.
        :param date after: Only list recordings logged after this datetime
        :param date before: Only list recordings logger before this datetime
        """
        pass

    def iter(self, to=None, from_=None, before=None, after=None):
        """
        Returns a page of :class:`SMSMessage` resources as a list. For paging informtion see :class:`ListResource`. 

        :param to: Only show SMS messages to this phone number.
        :param from_: Onlye show SMS message from this phone number.
        :param date after: Only list recordings logged after this datetime
        :param date before: Only list recordings logger before this datetime
        """
        pass

class SmsMessage(core.ListResource):
    
    pass

class Transcriptions(core.ListResource):

    pass

class Transcription(core.InstanceResource):
    
    pass

class Conferences(core.ListResource):
    
    def create(self):
        """
        Not supported, throws and exception
        """
        pass

    def list(self, status=None, friendly_name=None, updated_before=None,
             updated_after=None, created_after=None, created_before=None):
        """
        Return a list of :class:`Conference` resources

        :param status: Only show conferences with this status
        :param frienldy_name: Onlye show conferences with this exact frienldy_name
        :param date updated_after: Only list conferences updated after this datetime
        :param date updated_before: Only list conferences updated before this datetime
        :param date created_after: Only list conferences created after this datetime
        :param date created_before: Only list conferences created before this datetime
        """
        pass
    
class Conference(core.InstanceResource):
    
    pass

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

class Participant(core.InstanceResource):

    def mute(self):
        """
        Mute the participant
        """
        pass

    def unmute(self):
        """
        Unmute the participant
        """
        pass

    def kick(self):
        """
        Remove the participant from the given conference
        """
        pass

