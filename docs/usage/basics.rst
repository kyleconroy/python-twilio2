=====================
Accessing Resources
=====================

Authentication
-------------------------------

:class:`client.TwilioClient` needs your Twilio credentials. While these can be passed in directly to the construcutor, we suggest storing your credentials as environment variables. :class:`client.TwilioClient` looks for :const:`TWILIO_ACCOUT_SID` and :const:`TWILIO_AUTH_TOKEN` inside the current environment.

Here we look for the credentials in the enviroment

.. code-block:: python 
    
    from twilio.rest.client import TwilioClient

    conn = TwilioClient()

Where as here we pass the credentials into the constructor.

.. code-block:: python 
    
    from twilio.rest.client import TwilioClient

    ACCOUT_SID = "AXXXXXXXXXXXXXXXXX"
    AUTH_TOKEN = "YYYYYYYYYYYYYYYYYY"
    conn = TwilioClient(ACCOUNT_SID, AUTH_TOKEN)

