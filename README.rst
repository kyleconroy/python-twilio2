Installation
=============

We're listed on PyPi, so installation is one command away

.. code-block:: bash

    pip install twilio

You can also download the source and install

.. code-block:: bash

    python setup.py install

Examples
==========

REST API
---------

.. code-block:: python

    import twilio

    conn = twilio.api.Client()
    call = conn.calls.make(to="9991231234, from_="9991231234",
                           url="http://foo.com/call.xml")
    print call.length
    print call.sid


Twiml
-------

.. code-block:: python

    from twilio import twiml

    r = twiml.Response()
    r.play("monkey.mp3", loop=5)
    r.toxml() 
    # returns <Response><Play loop="3">monkey.mp3</Play><Response>

This module works great with various web frameworks
* Django
* AppEngine
* Flask

