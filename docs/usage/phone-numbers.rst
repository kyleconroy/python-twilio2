=================
Phone Numbers
=================

Search, buy, modify, and validate

Search
----------------
Find a number

Toll Free
^^^^^^^^^^^^^

Nothing really different, just talk about the things not supported


Buying a Number
-----------------

asdkfj

Changing URLS
---------------


Validate Caller Id
-----------------------
Adding a new phone number to your validated numbers is quick and easy

.. code-block:: python

    import twilio

    conn = twilio.api.Client()
    response = conn.caller_ids.validate("+9876543212")
    print response["validation_code"]

Twilio will call the provided number and for the  validation code to be entered.




