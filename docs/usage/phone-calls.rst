==============
Phone Calls
==============

Making a Phone Call
-------------------

The :class:`Calls` resource allows you to make outgoing calls::

    from twilio.rest import TwilioClient

    conn = TwilioClient()
    call = conn.calls.make(to="9991231234, from_="9991231234",
                           url="http://foo.com/call.xml")
    print call.length
    print call.sid

Accessing Specific Call Resources
----------------------------------------

The :class:`Call` resource has some sub resources you can access, such as notifications and recordings. If you have already have a :class:`Call` resource, they are easy to get.::

    from twilio.rest import TwilioClient

    conn = TwilioClient()
    calls = conn.calls.list()
    for c in calls:
        print c.notifications.list()
        print c.recordsings.list()
        print c.transcriptions.list()

Be careful, as the above code makes quite a few HTTP requests. However, what if you only have a Call Sid, and not the actual :class:`Resource`? No worries, as :meth:`list` can be passed a Call Sid as well.::

    from twilio.rest import TwilioClient

    conn = TwilioClient()
    sid = "CA24234"
    print conn.notifications.list(call=sid)
    print conn.recordsings.list(call=sid)
    print conn.transcriptions.list(call=sid)

Retrieve a Call Record
-------------------------

If you already have a :class:`Call` sid, you can use the client to retrieve that record.::

    from twilio.rest import TwilioClient

    conn = TwilioClient()
    sid = "CA12341234"
    call = conn.calls.get(sid)

Modifying Live Calls
--------------------

The :class:`Call` resource makes it easy to find current live calls and redirect them as necessary::

    from twilio.rest import TwilioClient

    conn = TwilioClient()
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

    from twilio.rest import TwilioClient

    conn = TwilioClient()
    sid = "CA12341234"
    conn.calls.update(sid, url="http://foo.com/new.xml", method=api.POST)

Handing up the call also works.::

    import twilio

    conn = twilio.api.Client()
    sid = "CA12341234"
    conn.calls.hangup(sid)

Recordings
--------------


Transcriptions
-----------------
