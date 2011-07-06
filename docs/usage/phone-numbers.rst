.. module:: twilio.rest.resources

=================
Phone Numbers
=================

With Twilio you can search and buy real phones numbers, just using the API.

Search
----------------

Finding numbers to buy couldn't be easier. We first search for a number in area code 530. Once we find one, we'll purchase it for our account.

.. code-block:: python

    from twilio.rest import TwilioClient

    conn = TwilioClient()
    numbers = conn.phone_numbers.search(area_code=530)

    if len(numbers) > 0:
        numbers[0].purchase()
    else:
        print "No numbers in 530 available"

Toll Free Numbers
^^^^^^^^^^^^^^^^^^^^^^^^

By default, :meth:`search` looks for local phone numbers. Set :data:`type` to ``tollfree`` to search toll-free numbers instead.

.. code-block:: python

    numbers = conn.phone_numbers.search(type="tollfree")

Numbers Containing Words
^^^^^^^^^^^^^^^^^^^^^^^^^^



.. code-block:: python

    numbers = conn.phone_numbers.search(type="tollfree")

You can search for numbers in other countries by passing the `ISO Country Code <>`_ as `country`. Currently only `US` and `CA` are supported.

:meth:`PhoneNumbers.search` method has plenty of other options to augment your search. See the API documentation for all available parameters.

Nothing really different, just talk about the things not supported


Buying a Number
-----------------

Changing URLS
---------------

Validate Caller Id
-----------------------
Twilio Adding a new phone number to your validated numbers is quick and easy

.. code-block:: python

    from twilio.rest import TwilioClient

    conn = TwilioClient()
    response = conn.caller_ids.validate("+9876543212")
    print response["validation_code"]

Twilio will call the provided number and for the  validation code to be entered.




