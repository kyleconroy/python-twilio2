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

    from twilio.rest import TwilioRestClient

    conn = TwilioRestClient()

If you'd rather not use enviroment variables, pass your account credentials directly to the the constructor.

.. code-block:: python

    from twilio.rest import TwilioRestClient

    ACCOUT_SID = "AXXXXXXXXXXXXXXXXX"
    AUTH_TOKEN = "YYYYYYYYYYYYYYYYYY"
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)


Listing Resources
-------------------

The :class:`TwilioRestClient` gives you access to various list resources. :meth:`ListResource.list`, by default, returns the most recent 50 instance resources.

.. code-block:: python

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient()
    resources = client.phone_calls.list()

:meth:`resource.ListResource.list` accepts paging arguments. The following will return page 3 with page size of 25.

.. code-block:: python

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient()
    resources = client.phone_calls.list(page=3, page_size=25)


Listing All Resources
^^^^^^^^^^^^^^^^^^^^^^^

Sometimes you'd like to retreive all records from a list resource. Instead of manually paging over the resource, the :class:`resources.ListResource.iter` method returns a generator. After exhausting the current page, the generator will request the next page of results.

.. warning:: Accessing all your records can be slow. We suggest only doing so when you absolutely need all the records

.. code-block:: python

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient()
    for number in client.phone_numbers.iter():
        print number.friendly_name


Get an Individual Resource
-----------------------------

To get an individual instance resource, use :class:`resources.ListResource.get`. Provide the :attr:`sid` of the resource you'd like to get.

.. code-block:: python

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient()

    call = client.calls.get("CA123")
    print call.sid

