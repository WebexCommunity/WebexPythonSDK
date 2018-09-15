.. _User API Doc:

.. currentmodule:: webexteamssdk

============
User API Doc
============


WebexTeamsAPI
=============

The :class:`WebexTeamsAPI` class creates "connection objects" for working with the Webex Teams APIs and hierarchically organizes the Webex Teams APIs and their endpoints underneath these connection objects.


.. include:: api_structure_table.rst


.. autoclass:: WebexTeamsAPI()
    :members:
    :exclude-members: access_token, base_url

    .. automethod:: WebexTeamsAPI.__init__


.. _people:

people
------

.. autoclass:: webexteamssdk.api.people.PeopleAPI()


.. _rooms:

rooms
-----

.. autoclass:: webexteamssdk.api.rooms.RoomsAPI()


.. _memberships:

memberships
-----------

.. autoclass:: webexteamssdk.api.memberships.MembershipsAPI()


.. _messages:

messages
--------

.. autoclass:: webexteamssdk.api.messages.MessagesAPI()


.. _teams:

teams
-----

.. autoclass:: webexteamssdk.api.teams.TeamsAPI()


.. _team_memberships:

team_memberships
----------------

.. autoclass:: webexteamssdk.api.team_memberships.TeamMembershipsAPI()


.. _webhooks:

webhooks
--------

.. autoclass:: webexteamssdk.api.webhooks.WebhooksAPI()


.. _organizations:

organizations
-------------

.. autoclass:: webexteamssdk.api.organizations.OrganizationsAPI()


.. _licenses:

licenses
--------

.. autoclass:: webexteamssdk.api.licenses.LicensesAPI()


.. _roles:

roles
-----

.. autoclass:: webexteamssdk.api.roles.RolesAPI()


.. _events:

events
------

.. autoclass:: webexteamssdk.api.events.EventsAPI()


.. _access_tokens:

access_tokens
-------------

.. autoclass:: webexteamssdk.api.access_tokens.AccessTokensAPI()


.. _Webex Teams Data Objects:

Webex Teams Data Objects
========================


.. _Person:

Person
------

.. autoclass:: Person()
    :inherited-members:


.. _Room:

Room
----

.. autoclass:: Room()
    :inherited-members:


.. _Membership:

Membership
----------

.. autoclass:: Membership()
    :inherited-members:


.. _Message:

Message
-------

.. autoclass:: Message()
    :inherited-members:


.. _Team:

Team
----

.. autoclass:: Team()
    :inherited-members:


.. _Team Membership:

Team Membership
---------------

.. autoclass:: TeamMembership()
    :inherited-members:


.. _Webhook:

Webhook
-------

.. autoclass:: Webhook()
    :inherited-members:


.. _WebhookEvent:

Webhook Event
-------------

.. autoclass:: WebhookEvent()
    :inherited-members:


.. _Organization:

Organization
------------

.. autoclass:: Organization()
    :inherited-members:


.. _License:

License
-------

.. autoclass:: License()
    :inherited-members:


.. _Role:

Role
----

.. autoclass:: Role()
    :inherited-members:


.. _Event:

Event
-----

.. autoclass:: Event()
    :inherited-members:


.. _Access Token:

Access Token
------------

.. autoclass:: AccessToken()
    :inherited-members:


.. _Exceptions:

Exceptions
==========

.. autoexception:: webexteamssdkException()
    :show-inheritance:
    :members:

.. autoexception:: AccessTokenError()
    :show-inheritance:
    :members:

.. autoexception:: ApiError()
    :show-inheritance:
    :members:

.. autoexception:: MalformedResponse()
    :show-inheritance:
    :members:

.. autoexception:: RateLimitError()
    :show-inheritance:
    :members:


.. _Warnings:

Warnings
========

.. autoexception:: RateLimitWarning()
    :show-inheritance:
    :members:


*Copyright (c) 2016-2018 Cisco and/or its affiliates.*
