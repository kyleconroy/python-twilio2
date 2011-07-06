.. module:: twilio.rest

=========================
Accessing REST Resources
=========================

To access Twilio REST resources, you'll first need to instantiate a :class:`TwilioClient`.

Authentication
--------------------------

The :class:`TwilioClient` needs your Twilio credentials. While these can be passed in directly to the construcutor, we suggest storing your credentials as environment variables. Why? You'll never have to worry about committing your credentials and accidently posting them somewhere public.

The :class:`TwilioClient` looks for :const:`TWILIO_ACCOUT_SID` and :const:`TWILIO_AUTH_TOKEN` inside the current environment.

With those two values set, create a new :class:`TwilioClient`.

.. code-block:: python

    from twilio.rest import TwilioClient

    conn = TwilioClient()

If you'd rather not use enviroment variables, pass your account credentials directly to the the constructor.

.. code-block:: python

    from twilio.rest import TwilioClient

    ACCOUT_SID = "AXXXXXXXXXXXXXXXXX"
    AUTH_TOKEN = "YYYYYYYYYYYYYYYYYY"
    conn = TwilioClient(ACCOUNT_SID, AUTH_TOKEN)
