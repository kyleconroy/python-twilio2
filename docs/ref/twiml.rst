.. _ref-twiml:

.. module:: twilio.twiml

==============
TwiML Creation
==============

Tutorial
---------------
The :mod:`twiml` module is responsible for the creation and validation of TwiML. Configuration options also allow users to specift defaults for various verbs.

Creation
^^^^^^^^

TwiML creation begins with the :class:`Response` verb. Each succesive verb is created by calling various methods on the response, such as :meth:`say` or :meth:`play`. These methods return the verbs they create to ease the creation of nested TwiML. To finish, call the :meth:`toxml` method on the :class:`Response`, which returns raw TwiML.::

    from twilio import twiml

    r = twiml.Response()
    r.say("Hello")
    r.toxml() 
    # returns <Response><Say>Hello</Say><Response>

The verb methods (outlined in the complete reference) take the body (only text) of the verb as the first argument. All attributes are keyword arguements.::

    from twilio import twiml

    r = twiml.Response()
    r.play("monkey.mp3", loop=5)
    r.toxml() 
    # returns <Response><Play loop="3">monkey.mp3</Play><Response>

Python 2.6+ added the :const:`with` statement for context management. Using :const:`with`, the module can *almost* emulate Ruby blocks.::

    from twilio import twiml

    r = twiml.Response()
    r.say("hello")
    with r.gather(end_on_key=4) as g:
        g.say("world")
    r.toxml() 

which returns::

    <Response>
      <Say>Hello</Say>
      <Gather endOnKey="4"><Say>World</Say></Gather>
    </Response>

Configuration
^^^^^^^^^^^^^

**THIS SECTION STILL TBD**

Usres may want to configure TwiML creation at a global scope. For example, make all :class:`Redirect` use the POST method by default. The :func:`config` function allows for easy custimization. Each verb also has a config method. See the complete reference for all the configuration options.::

    from twilio import twiml

    twiml.config(validation=False)
    twiml.redirect.config(method=POST)


Reference Guide
---------------

.. class:: Verb

   A TwiML :class:`Verb`

   .. method:: toxml()

      Return the XML that the Verb represents as a string.

Primary Verbs
^^^^^^^^^^^^^

.. class:: Response

   Returns a TwiML :class:`Response` object.

   .. method:: say(body="", **kwargs)

      Return a newly created :class:`Say` verb, nested inside this verb

   .. method:: play(body="", **kwargs)

      Return a newly created :class:`Play` verb, nested inside this verb

   .. method:: gather(**kwargs)

      Return a newly created :class:`Gather` verb, nested inside this verb

   .. method:: record(**kwargs)

      Return a newly created :class:`Record` verb, nested inside this verb

   .. method:: sms(body="", **kwargs)

      Return a newly created :class:`Sms` verb, nested inside this verb

   .. method:: dial(body="", **kwargs)

      Return a newly created :class:`Dial` verb, nested inside this verb

   .. method:: pause(**kwargs)

      Return a newly created :class:`Pause` verb, nested inside this verb

   .. method:: reject(**kwargs)

      Return a newly created :class:`Reject` verb, nested inside this verb

   .. method:: redirect(body="", **kwargs)

      Return a newly created :class:`Redirect` verb, nested inside this verb

   .. method:: hangup()

      Return a newly created :class:`Hangup` verb, nested inside this verb

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

Constants
^^^^^^^^^

Voices
>>>>>>
.. data:: MAN
.. data:: WOMAN

Languages
>>>>>>>>>
.. data:: ENGLISH
.. data:: SPANISH
.. data:: FRENCH
.. data:: GERMAN

HTTP Method
>>>>>>>>>>>
.. data:: GET
.. data:: POST

Rejection Reasons
>>>>>>>>>>>>>>>>>
.. data:: REJECTED
.. data:: BUSY























