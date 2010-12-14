.. _ref-api:

.. module:: twilio.api

==========
Twilio API
==========

This module will only work with Twilio's most recent API version `2010-04-01 <http://www.twilio.com/docs/api/2010-04-01/changelog>`_


Tutorial
>>>>>>>>

Making a connection
-------------------

The Twilio API Client will need your Twilio credentials. These can either be passed in directly or stored as environment variables with the name :const:`TWILIO_ACCOUT_SID` and :const:`TWILIO_AUTH_TOKEN`.::

    import twilio

    ACCOUT_SID = "AXXXXXXXXXXXXXXXXX"
    AUTH_TOKEN = "YYYYYYYYYYYYYYYYYY"
    conn = twilio.api.Client(ACCOUNT_SID, AUTH_TOKEN)

Huzzah, a new client is born.

It's all about Resources
------------------------

Just like the REST API, this api wrapper deals in the currency of resources

Buying a Phone Number
---------------------

Phone numbers can be bought via the :class:`PhoneNumber` resource::

    import twilio

    conn = twilio.api.Client()
    numbers = conn.phone_numbers.search(area_code=530, contains="WOLF")
    if numbers:
        number[0].purchase()


Making a Phone Call
-------------------

Sending an SMS
--------------

Routing a live call
-------------------

Updating Account Information
----------------------------

Checking Error Logs
-------------------

Something with Conferences
--------------------------

Reference
>>>>>>>>>

Base Classes
------------

.. class:: Client(account_sid=None, auth_token=None)

   The client has various :class:`ListResource` attached to it

.. class:: Resource

   .. method:: tohtml()

      Return the raw HTML of this :class:`Resource`

   .. method:: toxml()

      Return the raw XML of this :class:`Resource`

   .. method:: tojson()

      Return the raw JSON of this :class:`Resource`

   .. method:: tocsv()

      Return the raw CSV of this :class:`Resource`

   .. attribute:: uri

      The uri of this resource.

.. class:: ListResource

   A Twilio List resource

   .. method:: list(page=0)

      Returns a page of results from this list resource. Some instances of :class:`ListResource` accept filtering arguments

   .. method:: iter()

      Returns an iterator off all the items. Use with caution, as you very rareley need *all* of a single resource

   .. method:: count()

      Returns the number of resources

   .. method:: get(sid)

      Returns an :class:`InstanceResource` with a matching sid. Returns :const:`None` if no resource exists with that Sid.

.. class:: InstanceResource

   An instance of a single Twilio resource

   .. method:: update() 

   Change the contents of an instance resource. Analgous to :const:`PUT`

   .. method:: delete()

   Delete the given resource. Analgous to :const:`DELETE`

Specific List Resources
-----------------------

.. class:: PhoneNumbers

   .. method:: search(type=LOCAL, country="US", region=None, area_code=None, postal_code=None, near_number=None, near_lat_long=None, lata=None, rate_center=None, distance=25)

   :param type: Either :data:`LOCAL` or :data:`TOLL_FREE`. Defaults to :data:`LOCAL`
   :param area_code integer: 

Constancts
----------

Phone Number Types
******************
.. data:: LOCAL
.. data:: TOLL_FREE

