.. module:: twilio.rest

=====================
Phone Calls
=====================

The :class:`Calls` resource manages all interaction with Twilio phone calls, including the creation and termination of phone calls.

Making a Phone Call
-------------------

The :class:`Calls` resource allows you to make outgoing calls. Before a call can be successfully started, you'll need a url which outputs valid `TwiML <http://www.twilio.com/docs/api/twiml/>`_.

.. code-block:: python

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient()
    call = client.calls.make(to="9991231234, from_="9991231234")
                           url="http://foo.com/call.xml")
    print call.length
    print call.sid

Retrieve a Call Record
-------------------------

If you already have a :class:`Call` sid, you can use the client to retrieve that record.

.. code-block:: python

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient()
    sid = "CA12341234"
    call = client.calls.get(sid)

Accessing Specific Call Resources
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Each :class:`Call` resource also has access to its `notifications`, `recordings`, and `transcriptions`. These attributes are :class:`ListResources`, just like the :class:`Calls` resources itself.

.. code-block:: python

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient()
    sid = "CA12341234"
    call = client.calls.get(sid)

    print call.notifications.list()
    print call.recordsings.list()
    print call.transcriptions.list()

However, what if you only have a `CallSid`, and not the actual :class:`Resource`? No worries, as :meth:`list` can be filter based on `CallSid`.

.. code-block:: python

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient()
    sid = "CA24234"
    print client.notifications.list(call=sid)
    print client.recordsings.list(call=sid)
    print client.transcriptions.list(call=sid)


Modifying Live Calls
--------------------

The :class:`Call` resource makes it easy to find current live calls and redirect them as necessary

.. code-block:: python

    from twilio.rest import TwilioRestClient
    from twilio.rest.resources import Call

    client = TwilioRestClient()
    calls = client.calls.list(statsus=Call.IN_PROGRESS)
    for c in calls:
        c.route("http://foo.com/new.xml", method="POST")

Ending all live calls is also possible

.. code-block:: python

    from twilio.rest import TwilioRestClient
    from twilio.rest.resources import Call

    client = TwilioRestClient()
    calls = client.calls.list(status=Call.IN_PROGRESS)
    for c in calls:
        c.hangup()

Note that :meth:`hangup` will also cancel calls currently queued.

If you already have a :class:`Call` sid, you can use the :class:`Calls` resource to update
the record without having to use :meth:`get` first.

.. code-block:: python

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient()
    sid = "CA12341234"
    client.calls.update(sid, url="http://foo.com/new.xml", method="POST")

Handing up the call also works.

.. code-block:: python

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient()
    sid = "CA12341234"
    client.calls.hangup(sid)
