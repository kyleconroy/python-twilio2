.. _ref-resources-calls:

.. module:: twilio.api

Calls Resource
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

Reference
---------

.. class:: Calls

   .. method:: list(to=None, from_=None, status=None, before=None, after=None, page=0)

      Returns a page of :class:`Call` resources as a list. For paging informtion see :class:`ListResource`
   
      :param date after: Only list calls started after this datetime
      :param date before: Only list calls started before this datetime

   .. method:: iter(to=None, from_=None, status=None, before=None, after=None, page=0)

      Returns a iterator of **all** :class:`Call` resources. 
   
      :param date after: Only list calls started after this datetime
      :param date before: Only list calls started before this datetime


   .. method:: make(to, from_, url=None, method=None, fallback_url=None, fallback_method=None, status_callback=None, status_method=None, if_machine=None, timeout=60)

      Really just a wrapper for :meth:`create`

   .. method:: hangup(sid)

      Hangup a call with the associated sid.

   .. method:: route(sid, url=None, method=api.POST)

      Route the specified :class:`Call` to another url.

      :param sid: A Call Sid for a specific call
      :param url: A valid URL that returns TwiML. Twilio will immediately redirect the call to the new TwiML.
      :param method: The HTTP method Twilio should use when requesting the above URL. Defaults to POST.
      :returns: Updated :class:`Call` resource


.. class:: Call

   .. method:: hangup()

      Wrapper method for a :const:`PUT` with status set to :const:`COMPLETED`

   .. method:: route(url, method=POST)

      Wrapper method for a :const:`PUT` with url and method set

   .. attribute:: sid

      A 34 character string that uniquely identifies this resource.

   .. attribute:: parent_call_sid 

      A 34 character string that uniquely identifies the call that created this leg.

   .. attribute:: date_created

      The date that this resource was created, given as GMT in RFC 2822 format.

   .. attribute:: date_updated

      The date that this resource was last updated, given as GMT in RFC 2822 format.

   .. attribute:: account_sid

      The unique id of the Account responsible for creating this call.

   .. attribute:: to

      The phone number that received this call. e.g., +16175551212 (E.164 format)

   .. attribute:: from_ 

      The phone number that made this call. e.g., +16175551212 (E.164 format)

   .. attribute:: phone_number_sid

      If the call was inbound, this is the Sid of the IncomingPhoneNumber that received the call. If the call was outbound, it is the Sid of the OutgoingCallerId from which the call was placed.

   .. attribute:: status

      A string representing the status of the call. May be :data:`QUEUED`, :data:`RINGING`, :data:`IN-PROGRESS`, :data:`COMPLETED`, :data:`FAILED`, :data:`BUSY` or :data:`NO_ANSWER`.

   .. attribute:: start_time

      The start time of the call, given as GMT in RFC 2822 format. Empty if the call has not yet been dialed.

   .. attribute:: end_time
   
      The end time of the call, given as GMT in RFC 2822 format. Empty if the call did not complete successfully.

   .. attribute:: duration

      The length of the call in seconds. This value is empty for busy, failed, unanswered or ongoing calls.

   .. attribute:: price 
   
      The charge for this call in USD. Populated after the call is completed. May not be immediately available.

   .. attribute:: direction
   
      A string describing the direction of the call. inbound for inbound calls, outbound-api for calls initiated via the REST API or outbound-dial for calls initiated by a <Dial> verb.

   .. attribute:: answered_by

      If this call was initiated with answering machine detection, either human or machine. Empty otherwise.

   .. attribute:: forwarded_from

      If this call was an incoming call forwarded from another number, the forwarding phone number (depends on carrier supporting forwarding). Empty otherwise.

   .. attribute:: caller_name

      If this call was an incoming call from a phone number with Caller ID Lookup enabled, the caller's name. Empty otherwise.
