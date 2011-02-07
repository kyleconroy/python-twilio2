.. _ref-resources-accounts:

.. module:: twilio.api

Accounts Resource
==================

Updating Account Information
----------------------------

Updating :class:`Account` information is really easy::

    import twilio

    conn = twilio.api.Client()
    account = conn.accounts.get()
    account.update(name="My Awesome Account")

Creating a Sub Account
----------------------

    import twilio

    conn = twilio.api.Client()
    subaccount = conn.accounts.create(name="My Awesome SubAccount")

Can I make calls with this sub account? I have no idea

Reference
---------

.. class:: Accounts

   .. method:: get(sid=None)

      If no SID is provided, use the sid associated with the Twilio :class:`Client`

   .. method:: create(friendly_name=None)

      :param friendly_name: Update the human-readable description of this account.

      Returns a newly created sub account resource.

   .. method:: update(sid=None, friendly_name=None, status=None)

      :param sid: The sid of the account you are attempting to update. Defaults to the Account SID associated with the Client
      :param friendly_name: Update the human-readable description of this account.
      :param status: Alter the status of this account: use :data:`CLOSED` to irreversibly close this account, :data:`SUSPENDED` to temporarily suspend it, or :data:`ACTIVE` to reactivate it.


.. class:: Account

   .. method:: update(friendly_name=None, status=None)

      :param friendly_name: Update the human-readable description of this account.
      :param status: Alter the status of this account: use :data:`CLOSED` to irreversibly close this account, :data:`SUSPENDED` to temporarily suspend it, or :data:`ACTIVE` to reactivate it.


   .. attribute:: sid

      A 34 character string that uniquely identifies this account.

   .. attribute:: date_created

      The date that this account was created, in GMT in RFC 2822 format

   .. attribute:: date_updated

      The date that this account was last updated, in GMT in RFC 2822 format.

   .. attribute:: friendly_name

      A human readable description of this account, up to 64 characters long. By default the FriendlyName is your email address.

   .. attribute:: status

      The status of this account. Usually active, but can be suspended if you've been bad, or closed if you've been horrible.

   .. attribute:: auth_token

      The authorization token for this account. This token should be kept a secret, so no sharing.



