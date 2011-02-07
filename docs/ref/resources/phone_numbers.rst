.. _ref-resources-phone_numbers:

.. module:: twilio.api

Phone Numbers
=============

Buying a Phone Number
---------------------

Phone numbers can be bought via the :class:`PhoneNumbers` resource::

    import twilio

    conn = twilio.api.Client()
    numbers = conn.phone_numbers.search(area_code=530, contains="WOLF")
    if numbers:
        n = number[0]
        n = n.purchase(voice_url="http://foo.com/twiml.xml")
    else:
        print "No phone numbers found for that search"      

Note that the phone numbers returned from the search aren't :class:`PhoneNumber` resources, they are :class:`AvailablePhoneNumber` resources, so :meth:`purchase` returns the newly acquired :class:`PhoneNumber` resource.

Please see the :meth:`PhoneNumbers.search` and :meth:`PhoneNumbers.purchase` documentation for all available keyword arguements.

Buying a Phone Number in an Area Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To purchase a local phone number in a specific area code, no searching is required::

    conn = twilio.api.Client()
    n = conn.phone_numbers.purchase(area_code=456, 
                                    voice_url="http://foo.com/twiml.xml")
    print n.sid

Reference
---------

.. class:: PhoneNumbers

   .. method:: delete(sid)
   
      Release this phone number from your account. Twilio will no longer answer calls to this number, and you will stop being billed the monthly phone number fees. The phone number will eventually be recycled and potentially given to another customer, so use with care. If you make a mistake, contact us... we may be able to give you the number back.

   .. method:: list(phone_number=None, friendly_name=None)

      :param phone_number: Only return phone numbers that match this pattern. You can specify partial numbers and use '*' as a wildcard for any digit.
      :param friendly_name: Only return phone numbers with friendly names that exactly match this name.

   .. method:: purchase(phone_number=None, area_code=None, voice_url=None, voice_method=None, voice_fallback_url=None, voice_fallback_method=None, status_callback_method=None, sms_url=None, sms_method=None, sms_fallback_url=None, sms_fallback_method=None, voice_caller_id_lookup=False, account_sid=None)

      Attempt to purchase the specified number. The only required parameters are **either** phone_number or area_code

      :returns: Returns a :class:`PhoneNumber` instance on success, :data:`False` on failure

   .. method:: search(type="LOCAL", country="US", region=None, area_code=None, postal_code=None, near_number=None, near_lat_long=None, lata=None, rate_center=None, distance=25)

      :param type: Either :data:`LOCAL` or :data:`TOLL_FREE`. Defaults to :data:`LOCAL`
      :param integer area_code:

   .. method:: trasfer(sid, account_sid)

      Transfer the phone number with sid from the current account to another identified by account_sid

   .. method:: update(sid, api_version=None, voice_url=None, voice_method=None, voice_fallback_url=None, voice_fallback_method=None, status_callback_method=None, sms_url=None, sms_method=None, sms_fallback_url=None, sms_fallback_method=None, voice_caller_id_lookup=False, account_sid=None)

      Update this phone number instance

.. class:: PhoneNumber

   .. method:: delete()
   
      Release this phone number from your account. Twilio will no longer answer calls to this number, and you will stop being billed the monthly phone number fees. The phone number will eventually be recycled and potentially given to another customer, so use with care. If you make a mistake, contact us... we may be able to give you the number back.

   .. method:: transfer(account_sid)

      Transfer this phone number from the current account to another account identified by account_sid

   .. method:: update(api_version=None, voice_url=None, voice_method=None, voice_fallback_url=None, voice_fallback_method=None, status_callback_method=None, sms_url=None, sms_method=None, sms_fallback_url=None, sms_fallback_method=None, voice_caller_id_lookup=False, account_sid=None)

      Update this phone number

   .. attribute:: sid

      A 34 character string that uniquely idetifies this resource.

   .. attribute:: date_created

      The date that this resource was created, given as GMT RFC 2822 format.

   .. attribute:: date_updated

      The date that this resource was last updated, given as GMT RFC 2822 format.

   .. attribute:: friendly_name

      A human readable descriptive text for this resource, up to 64 characters long. By default, the FriendlyName is a nicely formatted version of the phone number.

   .. attribute:: account_sid

      The unique id of the Account responsible for this phone number.

   .. attribute:: phone_number

      The incoming phone number. e.g., +16175551212 (E.164 format)

   .. attribute:: api_version

      Calls to this phone number will start a new TwiML session with this API version.

   .. attribute:: voice_caller_id_lookup

      Look up the caller's caller-ID name from the CNAM database (additional charges apply). Either true or false.

   .. attribute:: voice_url

      The URL Twilio will request when this phone number receives a call.

   .. attribute:: voice_method

      The HTTP method Twilio will use when requesting the above Url. Either GET or POST.

   .. attribute:: voice_fallback_url

      The URL that Twilio will request if an error occurs retrieving or executing the TwiML requested by Url.

   .. attribute:: voice_fallback_method

      The HTTP method Twilio will use when requesting the VoiceFallbackUrl. Either GET or POST.

   .. attribute:: status_callback

      The URL that Twilio will request to pass status parameters (such as call ended) to your application.

   .. attribute:: status_callback_method

      The HTTP method Twilio will use to make requests to the StatusCallback URL. Either GET or POST.

   .. attribute:: sms_url

      The URL Twilio will request when receiving an incoming SMS message to this number.

   .. attribute:: sms_method

      The HTTP method Twilio will use when making requests to the SmsUrl. Either GET or POST.

   .. attribute:: sms_fallback_url

      The URL that Twilio will request if an error occurs retrieving or executing the TwiML from SmsUrl.

   .. attribute:: sms_fallback_method

      The HTTP method Twilio will use when requesting the above URL. Either GET or POST.

   .. attribute:: uri

      The URI for this resource, relative to https://api.twilio.com.

.. class:: AvailablePhoneNumber

   .. method:: purchase()

   Provision the phone number and then return the new :class:`PhoneNumber` instance.

   .. attribute:: friendly_name

      A nicely-formatted version of the phone number.

   .. attribute:: phone_number

      The phone number, in E.164 (i.e. "+1") format.

   .. attribute:: lata

      The LATA of this phone number.

   .. attribute:: rate_center

      The rate center of this phone number.

   .. attribute:: latitude

      The latitude coordinate of this phone number.

   .. attribute:: longitude

      The longitude coordinate of this phone number.

   .. attribute:: region

      The two-letter state or province abbreviation of this phone number.

   .. attribute:: postal_code

      The postal (zip) code of this phone number.

   .. attribute:: iso_country

      The ISO country code of this phone number.
