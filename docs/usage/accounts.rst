.. module:: twilio.rest

===========
Accounts
===========

Managing multiple Twilio accounts is nice and easy for stuff.

Updating Account Information
----------------------------

Use the :meth:`Account.update` to modify one of your accounts. Right now the only valid attribute is `FriendlyName`.

.. code-block:: python

    from twilio.rest.client import TwilioClient

    conn = TwilioClient()
    account = conn.accounts.get()
    account.update(name="My Awesome Account")

Creating Sub-Accounts
----------------------

Subaccounts are easy to make.

.. code-block:: python

    from twilio.rest.client import TwilioClient

    conn = TwilioClient()
    subaccount = conn.accounts.create(name="My Awesome SubAccount")


