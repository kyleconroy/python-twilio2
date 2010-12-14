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

The Twilio API Client will need your Twilio credentials. These can either be passed in directly or stored as environment variables with the name :const:`TWILIO_ACCOUT_SID` and :const:`TWILIO_AUTH_TOKEN`::

    import twilio

    ACCOUT_SID = "AXXXXXXXXXXXXXXXXX"
    AUTH_TOKEN = "YYYYYYYYYYYYYYYYYY"
    conn = twilio.api.Client(ACCOUNT_SID, AUTH_TOKEN)

Huzzah, a new client is born.

It's all about Resources
------------------------

Blah blah blah

Paging
------

Just like the REST API, this api wrapper deals in the currency of resources

Buying a Phone Number
---------------------

Phone numbers can be bought via the :class:`PhoneNumber` resource::

    import twilio

    conn = twilio.api.Client()
    numbers = conn.phone_numbers.search(area_code=530, contains="WOLF")
    if numbers:
        n = number[0]

    n = n.purchase()
    n.update(voice_url="http://foo.com/twiml.xml")

Note that the phone numbers returned from the search aren't actual :class:`PhoneNumber` resources, so :meth:`purchase` returns the newly acquired :class:`PhoneNumber` resource.

Please the the :meth:`search` documentation for all supported keyword arguements.

Making a Phone Call
-------------------

The :class:`Calls` resource allows you to make outgoing calls::

    import twilio

    conn = twilio.api.Client()
    call = conn.calls.make(to="9991231234, from_="9991231234",
                           url="http://foo.com/call.xml")
    print call.length

Accessing Resources from a specific Call
----------------------------------------

The :class:`Call` resource has some sub resources you can access, such as notifications and recordings. If you have already have a :class:`Call` resource, they are easy to get.::

    import twilio

    conn = twilio.api.Client()
    calls = conn.calls.list()
    for c in calls:
        print c.notifications.list()
        print c.recordsings.list()
        print c.transcriptions.list()

Be careful, as the above code makes quite a few HTTP requests. However, what if you only have a Call Sid, and not the actual :class:`Resource`? No worries, as :meth:`list` can be passed a Call Sid as well.::

    import twilio

    conn = twilio.api.Client()
    sid = "CA24234"
    print conn.notifications.list(call=sid)
    print conn.recordsings.list(call=sid)
    print conn.transcriptions.list(call=sid)

Routing a live call
-------------------

The :class:`Calls` resource makes it easy to find current live calls and redirect them as necessary::

    import twilio

    conn = twilio.api.Client()
    calls = conn.calls.list(statsus=api.IN_PROGRESS)
    for c in calls:
        c.route("http://foo.com/new.xml", method=api.POST)

Ending all live calls is also possible::

    import twilio

    conn = twilio.api.Client()
    calls = conn.calls.list(statsus=api.IN_PROGRESS)
    for c in calls:
        c.hangup()

Note that :meth:`hangup` will also cancel calls currently queued.

Sending and Retreiving SMS Messages
-----------------------------------

The :class:`SmsMessages` resource makes it easy to send SMS messages::

    import twilio

    conn = twilio.api.Client()
    msg = conn.sms.send(to=8995431234, from_=3452341231,
                        body="Hello Monkey")

It's also easy to get your messages back::

    import twilio

    conn = twilio.api.Client()
    messages = conn.sms.list(to=3453453344)
    for m in messages:
        print m.body

Updating Account Information
----------------------------

Updating :class:`Account` information is really easy::

    import twilio

    conn = twilio.api.Client()
    account = conn.accounts.get()
    account.update(name="My Awesome Account")

Accessing Sub Accounts
----------------------------

Getting information on all your sub-accounts is easy.::

    import twilio

    conn = twilio.api.Client()
    accounts = conn.accounts.list()
    for a in accounts:
        print a.status

Checking Error Logs
-------------------

The :class:`Notificatoins` resource holds all log entries for your account

Something with Conferences
--------------------------

Reference
>>>>>>>>>

Base Classes
------------

.. class:: Client(account_sid=None, auth_token=None)

   The client has various :class:`ListResource` attached to it

.. class:: Resource

   .. method:: to_html()

      Return the raw HTML of this :class:`Resource`

   .. method:: to_xml()

      Return the raw XML of this :class:`Resource`

   .. method:: to_json()

      Return the raw JSON of this :class:`Resource`

   .. method:: to_csv()

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

   .. method:: create()

      Returns a new :class:`InstanceResource`. Analgous to :const:`POST`

   .. method:: get(sid)

      Returns an :class:`InstanceResource` with a matching sid. Returns :const:`None` if no resource exists with that Sid.

.. class:: InstanceResource

   An instance of a single Twilio resource

   .. method:: delete()

   Delete the given resource. Analgous to :const:`DELETE`

   .. method:: update() 

   Change the contents of an instance resource. Analgous to :const:`PUT`


Specific List Resources
-----------------------

.. class:: Accounts

   .. method:: get(sid=None)

      If no SID is provided, use the sid associated with the Twilio :class:`Client`

.. class:: Calls

   .. method:: list(to=None, from_=None, status=None, before=None, after=None)

      Returns a list of :class:`Call` resources. For paging informtion see :class:`ListResource`
   
      :param date after:
      :param date before:

   .. method:: make(to, from_, url=None, method=None, fallback_url=None, fallback_method=None, status_callback=None, status_method=None, if_machine=None, timeout=60)

      Really just a wrapper for :meth:`create`

.. class:: PhoneNumbers

   .. method:: search(type=LOCAL, country="US", region=None, area_code=None, postal_code=None, near_number=None, near_lat_long=None, lata=None, rate_center=None, distance=25)

      :param type: Either :data:`LOCAL` or :data:`TOLL_FREE`. Defaults to :data:`LOCAL`
      :param integer area_code:  

.. class:: Recordings

   .. method:: list(call=None, before=None, after=None)

      :param call: A Call Sid for a specific call
      :param date after:
      :param date before: 

.. class:: Transcriptions

   .. method:: list(call=None, before=None, after=None)

      :param call: A Call Sid for a specific call
      :param date after:
      :param date before:

.. class:: Participants

   .. method:: list(conference, muted=None)

      Note that the conference Sid is **required**. You can only access participants in the conference through the conference resource, so this has to be a little bit different

   .. method:: get(conference, participant)

      Note that the conference Sid is **required**. You can only access participants in the conference through the conference resource, so this has to be a little bit different

.. class:: SmsMessages

   .. method:: list(to=None, from_=None, before=None, after=None)

      Note: Why can't we filter on SMS status?

      Returns a list of :class:`SMS` resources. For paging informtion see :class:`ListResource`
   
      :param date after:
      :param date before:

   .. method:: send(to=None, from_=None, url=None, status_callback=None)

      Again, this is just a wrapper for a call to :meth:`create`

   

Specific Instance Resources
---------------------------

Attributes for all :class:`InstanceResource` objects are the same as their corresponding resource in the `REST API <http://www.twilio.com/docs/api/rest/>`_.

.. class:: Call

   .. method:: hangup()

      Wrapper method for a :const:`PUT` with status set to :const:`COMPLETED`

   .. method:: route(url, method=POST)

      Wrapper method for a :const:`PUT` with url and method set

.. class:: AvailablePhoneNumber

   .. method:: purchase()

   Provision the phone number and then return the new :class:`PhoneNumber` instance.

Constants
----------

Phone Number Types
******************
.. data:: LOCAL
.. data:: TOLL_FREE

Call Status
***********
.. data:: QUEUED
.. data:: RINGING
.. data:: IN_PROGRESS
.. data:: COMPLETED
.. data:: FAILED
.. data:: BUSY
.. data:: NO_ANSWER

HTTP VERBS
**********
.. data:: GET
.. data:: POST
.. data:: PUT
.. data:: DELETE


