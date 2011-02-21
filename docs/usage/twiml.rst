.. _usage-twiml:

.. module:: twilio.twiml

==============
TwiML Creation
==============

TwiML creation begins with the :class:`Response` verb. Each succesive verb is created by calling various methods on the response, such as :meth:`say` or :meth:`play`. These methods return the verbs they create to ease the creation of nested TwiML. To finish, call the :meth:`toxml` method on the :class:`Response`, which returns raw TwiML.

.. code-block:: python

    from twilio import twiml

    r = twiml.Response()
    r.say("Hello")
    r.toxml() 
    # returns <Response><Say>Hello</Say><Response>

The verb methods (outlined in the complete reference) take the body (only text) of the verb as the first argument. All attributes are keyword arguements.

.. code-block:: python

    from twilio import twiml

    r = twiml.Response()
    r.play("monkey.mp3", loop=5)
    r.toxml() 
    # returns <Response><Play loop="3">monkey.mp3</Play><Response>

Python 2.6+ added the :const:`with` statement for context management. Using :const:`with`, the module can *almost* emulate Ruby blocks.

.. code-block:: python

    from twilio import twiml

    r = twiml.Response()
    r.say("hello")
    with r.gather(end_on_key=4) as g:
        g.say("world")
    r.toxml() 

which returns

.. code-block:: xml

    <Response>
      <Say>Hello</Say>
      <Gather endOnKey="4"><Say>World</Say></Gather>
    </Response>

