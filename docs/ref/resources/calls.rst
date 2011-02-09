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

