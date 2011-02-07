.. _ref-resources-caller_ids:

.. module:: twilio.api

Caller Ids Resource
===================

Validate a Phone Number
-----------------------
Adding a new phone number to your validated numbers is quick and easy::

    import twilio

    conn = twilio.api.Client()
    response = conn.caller_ids.validate("+9876543212")
    print response["validation_code"]

Twilio will call the provided number and for the  validation code to be entered.

Listing all Validated Phone Numbers
-----------------------------------
Show all the current caller_ids::

    import twilio

    conn = twilio.api.Client()
    for caller_id in conn.caller_ids.list():
        print caller_id.friendly_name

Reference
---------

.. class:: CallerIds

   .. method:: delete(sid)

      Deletes a specific :class:`CallerId` from the account.

   .. method:: list(phone_number=None, friendly_name=None)
   
      :param phone_number: Only show the caller id resource that exactly matches this phone number.
      :param friendly_name: Only show the caller id resource that exactly matches this name.

   .. method:: update(sid, friendly_name=None)

      Update a specific :class:`CallerId`

   .. method:: validate(phone_number, friendly_name=None, call_delay=0, extension=None)

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

.. class:: CallerId

   .. method:: delete()

      Deletes the caller ID from the account.

   .. method:: update(friendly_name=None)

      Update the CallerId

   .. attribute:: sid

      A 34 character string that uniquely identifies this resource.

   .. attribute:: date_created

      The date that this resource was created, given in RFC 2822 format.

   .. attribute:: date_updated

      The date that this resource was last updated, given in RFC 2822 format.

   .. attribute:: friendly_name

      A human readable descriptive text for this resource, up to 64 characters long. By default, the FriendlyName is a nicely formatted version of the phone number.

   .. attribute:: account_sid

      The unique id of the Account responsible for this Caller Id.

   .. attribute:: phone_number

      The incoming phone number. Formatted with a '+' and country code e.g., +16175551212 (E.164 format).

   .. attribute:: uri

      The URI for this resource, relative to https://api.twilio.com.

