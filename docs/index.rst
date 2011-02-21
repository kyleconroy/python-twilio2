.. twilio-python2 documentation master file, created by
   sphinx-quickstart on Mon Dec 13 16:47:32 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================
The Twilio Python Library
==================================

The **twilio-python** helper library simplifies interaction with Twilio's `REST API <http://www.twilio.com/docs/api/twiml/>`_ and facilitates creation of valid `TwiML <http://www.twilio.com/docs/api/twiml/>`_.


Installation
================

**twilio-python** is listed on `PyPi <http://pypi.python.org/pypi>`_, so just use :data:`pip`

.. code-block:: bash

    pip install twilio

You can also download the source and install using :data:`setuptools`

.. code-block:: bash

    python setup.py install

Getting Started
================

.. toctree::
    :maxdepth: 1

    getting-started
    

User Guide
==================

.. toctree::
    :maxdepth: 2

    usage/basics
    usage/twiml
    usage/phone-calls
    usage/phone-numbers
    usage/messages
    usage/conferences
    usage/accounts
    usage/notifications

API Reference
==================

A complete guide to all public APIs found in `twilio-python`

.. toctree::
    :maxdepth: 2

    api

Support and Development
==========================
All development occurs over on `Github <https://github.com/twilio/twilio-python>`_. To checkout the source, 

.. code-block:: bash

    git clone git@github.com:twilio/twilio-python.git


Report bugs using the Github `issue tracker <https://github.com/twilio/twilio-python/issues>`_.

If you’ve got questions that aren’t answered by this documentation, ask the `#twilio IRC channel <irc://irc.freenode.net/#twilio>`_

Changelog
=================
Current stable version is 3.0.0.

.. toctree::
   :maxdepth: 1

   changelog

This project uses `semantic versioning <http://semver.org/>`_.


