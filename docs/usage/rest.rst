.. _ref-rest

.. module:: twilio.rest.resources

REST API Usage
>>>>>>>>>>>>>>>

Accounts 
==================

Updating Account Information
----------------------------

Updating :class:`Account` information is really easy::

    import twilio

    conn = twilio.api.Client()
    account = conn.accounts.get()
    account.update(name="My Awesome Account")

Creating a Sub Account
----------------------

.. code-block:: python

    import twilio

    conn = twilio.api.Client()
    subaccount = conn.accounts.create(name="My Awesome SubAccount")

Can I make calls with this sub account? I have no idea

Phone Calls
==============

Making a Phone Call
-------------------

The :class:`Calls` resource allows you to make outgoing calls::

    import twilio

    conn = twilio.api.Client()
    call = conn.calls.make(to="9991231234, from_="9991231234",
                           url="http://foo.com/call.xml")
    print call.length
    print call.sid

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

Retrieve a Call Record
----------------------

If you already have a :class:`Call` sid, you can use the client to retrieve that record.::

    import twilio
    
    conn = twilio.api.Client()
    sid = "CA12341234"
    call = conn.calls.get(sid)

Modifying live calls
--------------------

The :class:`Call` resource makes it easy to find current live calls and redirect them as necessary::

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

If you already have a :class:`Call` sid, you can use the :class:`Calls` resource to update
the record without having to use :meth:`get` first.::

    import twilio
    
    conn = twilio.api.Client()
    sid = "CA12341234"
    conn.calls.update(sid, url="http://foo.com/new.xml", method=api.POST)

Handing up the call also works.::

    import twilio
    
    conn = twilio.api.Client()
    sid = "CA12341234"
    conn.calls.hangup(sid)



Caller Ids
=============

Validate a Phone Number
-----------------------
Adding a new phone number to your validated numbers is quick and easy

.. code-block:: python

    import twilio

    conn = twilio.api.Client()
    response = conn.caller_ids.validate("+9876543212")
    print response["validation_code"]

Twilio will call the provided number and for the  validation code to be entered.

Listing all Validated Phone Numbers
-----------------------------------
Show all the current caller_ids

.. code-block:: python

    import twilio

    conn = twilio.api.Client()
    for caller_id in conn.caller_ids.list():
        print caller_id.friendly_name

Conferences
================

Filter Conferences by Status
---------------------------------

.. code-block:: python

    import twilio

    conn = twilio.api.Client()
    for c in conn.conferences.list(status="in-progress"):
        print c.sid

Mute all participants
----------------------

.. code-block:: python

    import twilio
    conference = "CO119231312"

    conn = twilio.api.Client()
    for p in conn.participants.list(conference):
        p.mute()

Notifications 
=================

Filter Notifications by Log Level
---------------------------------

.. code-block:: python

    import twilio

    conn = twilio.api.Client()
    for n in conn.notifications.list(log_level=0):
        print n.error_code

SMS Messages
==============

Sending a SMS Message
----------------------

The :class:`SmsMessages` resource allows you to send outgoing text messages

.. code-block:: python

    import twilio

    conn = twilio.api.Client()
    t = "9991231234
    f ="9991231234"
    text = "Hello monkey!"
    message = conn.sms.messages.create(to=t, from_=f, body=text)
    print message.sid

Transcriptions
=================

Show all Transcribed Messages
---------------------------------

.. code-block:: python

    import twilio

    conn = twilio.api.Client()
    for t in conn.transcriptions.list():
        print t.transcription_text
