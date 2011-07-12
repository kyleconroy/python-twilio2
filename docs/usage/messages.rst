.. module:: twilio.rest.resources

============
SMS Messages
============

For more information, see the `SMS Message REST Resource <http://www.twilio.com/docs/api/rest/sms>`_ documentation.

Sending a Text Message
----------------------

Send a text message in only a few lines of code

.. code-block:: python

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient()

    message = client.sms.messages.create(to="+13216851234",
                                         from_="+15555555555",
                                         body="Hello!")

A word of warning: The message body must be less than 160 characters in length


Retrieving Sent Messages
-------------------------

.. code-block:: python

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient()

    for message in client.sms.messages.list():
        print message.body


Filtering Your Messages
-------------------------

The :meth:`list` methods supports filtering on :attr:`to`, :attr:`from_`, and :attr:`date_sent`. The following will only show messages to "+5466758723" on January 1st, 2011.

.. code-block:: python

    from datetime import date
    from twilio.rest import TwilioRestClient

    client = TwilioRestClient()

    messages = client.sms.messages.list(to="+5466758723",
                                        date_sent=date(2011,1,1))

    for message in messages:
        print message.body


Short Codes
--------------
Not supported just yet, as `Twilio Short Code <http://www.twilio.com/sms/short-codes>`_
is still in beta. You can sign up to be notified when short codes launch.
