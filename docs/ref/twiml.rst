.. _ref-twiml:

.. module:: twilio.twiml


Reference Guide
---------------

.. class:: Verb

   A TwiML :class:`Verb`

   .. method:: toxml()

      Return the XML that the Verb represents as a string.

Primary Verbs
^^^^^^^^^^^^^

.. class:: Say(body, voice="man", langauge="en", loop=1)

   The :class:`Say` verb converts text to speech that is read back to the caller.

   .. attribute:: voice

      The :attr:`voice` attribute allows you to choose a male or female voice to read text back. The default value is 'man'.

   .. attribute:: language

      The :attr:`language` attribute allows you pick a voice with a specific language's accent and pronunciations. Twilio currently supports languages 'en' (English), 'es' (Spanish), 'fr' (French), and 'de' (German). The default is 'en'.

   .. attribute:: loop

      The :attr:`loop` attribute specifies how many times you'd like the text repeated. The default is once. Specifying '0' will cause the the :class:`Say` verb to loop until the call is hung up.


.. class:: Play(url="", loop=1)

   .. attribute:: url

   .. attribute:: loop

      The :attr:`loop` attribute specifies how many times you'd like the text repeated. The default is once. Specifying '0' will cause the the :class:`Say` verb to loop until the call is hung up.

.. class:: Gather(action=None, method="POST", timeout=5, finish_on_key="#", num_digits=None)

   .. method:: say(body="", **kwargs)

      Return a newly created :class:`Say` verb, nested inside this verb

   .. method:: play(body="", **kwargs)

      Return a newly created :class:`Play` verb, nested inside this verb

   .. method:: pause(**kwargs)

      Return a newly created Pause verb, nested inside this verb

   .. attribute:: action

   .. attribute:: method

   .. attribute:: timeout

   .. attribute:: finish_on_key

   .. attribute:: num_digits

.. class:: Record(action=None, method="POST", timeout=5, finish_on_key="#", max_length=3600, transcribe=False, transcribe_callback=None, play_beep=True)

.. class:: Sms(to, from_, action=None, method=POST, status_callback=None)

.. class:: Dial(body="", action=None, method=POST, timeout=30, hangup_on_star=False, time_limit=14400, caller_id=None)

   .. method:: number(body="", **kwargs)

      Return a newly created :class:`Number` noun, nested inside this verb

   .. method:: conference(body="", **kwargs)

      Return a newly created :class:`Conference` noun, nested inside this verb


Seconday Verbs
^^^^^^^^^^^^^^

.. class:: Pause(length=1)

   .. attribute:: length

   The 'length' attribute specifies how many seconds Twilio will wait silently before continuing on.

.. class:: Reject(reason="rejected")

   .. attribute:: reason

   Allowed values include "rejected" and "busy"

.. class:: Redirect(body="", method=POST)

.. class:: Hangup()


Nouns
^^^^^^^^^^^^^

.. class:: Conference(body, muted=False, beep=True, stat_on_enter=True, end_on_exit=False, wait_url=None, wait_method="POST")

.. class:: Number(phone, send_digits=None, url=None)























