.. module:: twilio.rest.resources

=================
Applications
=================

An application inside of Twilio is just a set of URLs and other configuration data that tells Twilio how to behave when one of your Twilio numbers receives a call or SMS message.

For more information, see the `Application REST Resource <http://www.twilio.com/docs/api/rest/applications>`_ documentation.


Creating an Application
---------------------------


.. code-block:: python

    from twilio.rest import TwilioRestClient

    conn = TwilioRestClient()
    numbers = conn.applications.create()

Toll Free Numbers
^^^^^^^^^^^^^^^^^^^^

By default, :meth:`search` looks for local phone numbers. Set :data:`type` to ``tollfree`` to search toll-free numbers instead.

.. code-block:: python

    numbers = conn.phone_numbers.search(type="tollfree")


Numbers Containing Words
^^^^^^^^^^^^^^^^^^^^^^^^^^

Phone number search also supports looking for words inside phone numbers. The following example will find any phone number with "FOO" in it.

.. code-block:: python

    numbers = conn.phone_numbers.search(contains="FOO")

You can use the ''*'' wildcard to match any character. The following example finds any phone number that matches the pattern ''D*D''.

.. code-block:: python

    numbers = conn.phone_numbers.search(contains="D*D")

:meth:`PhoneNumbers.search` method has plenty of other options to augment your search. The `AvailablePhoneNumbers REST Resource <http://www.twilio.com/docs/api/rest/available-phone-numbers>`_ documentation also documents the various search options.


Buying a Number
---------------

If you've found a phone numnber you want, you can purchase the number

.. code-block:: python

    from twilio.rest import TwilioRestClient

    conn = TwilioRestClient()
    number = conn.phone_numbers.purchase("+15305431234")

However, it's easier to purchase numbers after finding them using search (as shown in the first example).


Changing Applications
----------------------

An :class:`Application` encapsulates all necessary URLs for use with phone numbers. Update an application on a phone number using :meth:`update`.

.. code-block:: python

    from twilio.rest import TwilioRestClient

    phone_sid = "PNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    conn = TwilioRestClient()
    number = conn.phone_numbers.update(phone_sid, application="AP123")

See :doc:`/usage/applications` for instrucitons on updating and mantaining Applications.

Validate Caller Id
-----------------------
Twilio Adding a new phone number to your validated numbers is quick and easy

.. code-block:: python

    from twilio.rest import TwilioRestClient

    conn = TwilioRestClient()
    response = conn.caller_ids.validate("+9876543212")
    print response["validation_code"]

Twilio will call the provided number and wait for the  validation code to be entered.




