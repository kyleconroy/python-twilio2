.. module:: twilio.rest.resources

==============================
Conferences and Participants
==============================

For more information, see the `Conference REST Resource <http://www.twilio.com/docs/api/rest/conference>`_ and `Participant REST Resource <http://www.twilio.com/docs/api/rest/conference>`_ documentation.

Listing Conferences
-----------------------

.. code-block:: python

    from twilio.rest import TwilioClient

    conn = TwilioClient()
    conferences = conn.conferences.list()

    for conference in conferences:
        print conference.sid

Filtering Conferences
-----------------------

The :meth:`Conferences.list` method supports filtering on :attr:`status`, :attr:`date_updated`, :attr:`date_created` and :attr:`friendly_name`. The following code will return a list of all active conferences and print their friendly name.

.. code-block:: python

    from twilio.rest import TwilioClient

    conn = TwilioClient()
    conferences = conn.conferences.list(status="active")

    for conference in conferences:
        print conference.friendly_name


Listing Participants
----------------------

Each :class:`Conference` has a :attr:`participants` instance which represents all current users in the conference

.. code-block:: python

    from twilio.rest import TwilioClient

    conn = TwilioClient()
    conference = conn.conferences.get("CF123")

    for participant in conference.participants.list():
        print participant.sid

Managing Participants
----------------------

Each :class:`Conference` has a :attr:`participants` function that returns a
:class:`Participants` instance. This behaviour differs from other list resources
because :class:`Participants` needs a participant sid AND a conference sid to access the participants resource.

Participants can be either muted or kicked out of the conference. The following code kicks out the first participants and mutes the rest.

.. note::

.. code-block:: python

    from twilio.rest import TwilioClient

    conn = TwilioClient()
    participants = conn.participants("CF123").list()

    if len(participants) == 0:
        return

    # Kick the first person out
    participants.pop().kick()

    # And mute the rest
    for participant in participants:
        participant.mute()
