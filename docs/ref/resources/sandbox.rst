.. _ref-resources-calls:

.. module:: twilio.api

Sandbox Resource
=================

Unlike the other resources at Twilio, the Sandbox exists as a singleton. Accessing this resource is a bit different

.. code-block:: python

    import twilio

    conn = twilio.api.Client()
    sandbox = conn.sandbox.get()
    print sandbox.pin

Updating your sandbox doesn't require a sid

.. code-block:: python

    import twilio

    conn = twilio.api.Client()
    sandbox = conn.sandbox.update(voice_url="https://foo.com/twiml.xml")

However, you can't access attributes using the sandbox object on the client. You must access the object via :meth:`Sandbox.get`

.. code-block:: python

    import twilio

    conn = twilio.api.Client()
    print conn.sandbox.pin
    AttributeError: 'sandbox' object has no attribute 'pin'


Reference
---------

.. class:: Sandbox

   .. method:: get()

      Return the Sandbox object

   .. method:: update(voice_url=None, voice_method="POST", sms_url=None, sms_method="POST")

      Update your Sandbox

   .. attribute:: pin

      An 8 digit number that gives access to this sandbox.

   .. attribute:: account_sid

      The unique id of the Account connected to this sandbox.

   .. attribute:: phone_number

      The phone number of the sandbox.  Formatted with a '+' and country code e.g., +16175551212 (E.164 format).

   .. attribute:: voice_url

      The URL Twilio will request when the sandbox number is called.

   .. attribute:: voice_method

      The HTTP method to use when requesting the above URL. Either GET or POST.

   .. attribute:: sms_url

      The URL Twilio will request when receiving an incoming SMS message to the sandbox number.

   .. attribute:: sms_method

      The HTTP method to use when requesting the sms URL. Either GET or POST.

   .. attribute:: date_created

      The date that this resource was created, given in RFC 2822 format.

   .. attribute:: date_updated

      The date that this resource was last updated, given in RFC 2822 format.

   .. attribute:: uri

      The URI for this resource, relative to https://api.twilio.com
