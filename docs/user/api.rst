.. _User API Doc:

.. currentmodule:: webexpythonsdk

============
User API Doc
============


WebexAPI
=============

The :class:`WebexAPI` class creates "connection objects" for working with the Webex APIs and hierarchically organizes the Webex APIs and their endpoints underneath these connection objects.


.. include:: api_structure_table.rst


.. autoclass:: WebexAPI()
    :members:
    :exclude-members: access_token, base_url

    .. automethod:: WebexAPI.__init__


.. _access_tokens:

access_tokens
-------------

.. autoclass:: webexpythonsdk.api.access_tokens.AccessTokensAPI()


.. _admin_audit_events:

admin_audit_events
------------------

.. autoclass:: webexpythonsdk.api.admin_audit_events.AdminAuditEventsAPI()


.. _attachment_actions:

attachment_actions
------------------

.. autoclass:: webexpythonsdk.api.attachment_actions.AttachmentActionsAPI()


.. _events:

events
------

.. autoclass:: webexpythonsdk.api.events.EventsAPI()


.. _guest_issuer:

guest_issuer
------------

.. autoclass:: webexpythonsdk.api.guest_issuer.GuestIssuerAPI()


.. _licenses:

licenses
--------

.. autoclass:: webexpythonsdk.api.licenses.LicensesAPI()


.. _memberships:

memberships
-----------

.. autoclass:: webexpythonsdk.api.memberships.MembershipsAPI()


.. _messages:

messages
--------

.. autoclass:: webexpythonsdk.api.messages.MessagesAPI()


.. _organizations:

organizations
-------------

.. autoclass:: webexpythonsdk.api.organizations.OrganizationsAPI()


.. _people:

people
------

.. autoclass:: webexpythonsdk.api.people.PeopleAPI()


.. _roles:

roles
-----

.. autoclass:: webexpythonsdk.api.roles.RolesAPI()


.. _rooms:

rooms
-----

.. autoclass:: webexpythonsdk.api.rooms.RoomsAPI()


.. _teams:

teams
-----

.. autoclass:: webexpythonsdk.api.teams.TeamsAPI()


.. _team_memberships:

team_memberships
----------------

.. autoclass:: webexpythonsdk.api.team_memberships.TeamMembershipsAPI()


.. _webhooks:

webhooks
--------

.. autoclass:: webexpythonsdk.api.webhooks.WebhooksAPI()


.. _Webex Data Objects:

Webex Data Objects
==================


.. _Access Token:

Access Token
------------

.. autoclass:: AccessToken()
    :inherited-members:


.. _Admin_Audit_Event:

Admin Audit Event
-----------------

.. autoclass:: AdminAuditEvent()
    :inherited-members:


.. _Attachment Action:

Attachment Action
-----------------

.. autoclass:: AttachmentAction()
    :inherited-members:


.. _Event:

Event
-----

.. autoclass:: Event()
    :inherited-members:


.. _Guest_Issuer_Token:

Guest Issuer Token
------------------

.. autoclass:: GuestIssuerToken()
    :inherited-members:


.. _License:

License
-------

.. autoclass:: License()
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


.. _Organization:

Organization
------------

.. autoclass:: Organization()
    :inherited-members:


.. _Person:

Person
------

.. autoclass:: Person()
    :inherited-members:


.. _Role:

Role
----

.. autoclass:: Role()
    :inherited-members:


.. _Room:

Room
----

.. autoclass:: Room()
    :inherited-members:


.. _RoomMeetingInfo:

Room Meeting Info
-----------------

.. autoclass:: RoomMeetingInfo()
    :inherited-members:


.. _Team:

Team
----

.. autoclass:: Team()
    :inherited-members:


.. _TeamMembership:

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


.. _Exceptions:

Exceptions
==========

.. autoexception:: webexpythonsdkException()
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

.. autoexception:: webexpythonsdkWarning()
    :show-inheritance:
    :members:

.. autoexception:: ApiWarning()
    :show-inheritance:
    :members:

.. autoexception:: RateLimitWarning()
    :show-inheritance:
    :members:

.. _CardsAPI:

Cards and Buttons
=================

.. autoclass:: webexpythonsdk.cards.card.AdaptiveCard()

Components
----------

.. autoclass:: webexpythonsdk.cards.components.Image()
   :members:

   .. automethod:: __init__

.. autoclass:: webexpythonsdk.cards.components.TextBlock()
   :members:

   .. automethod:: __init__

.. autoclass:: webexpythonsdk.cards.components.Column()

.. autoclass:: webexpythonsdk.cards.components.Fact()

.. autoclass:: webexpythonsdk.cards.components.Choice()

Options
-------

.. autoclass:: webexpythonsdk.cards.options.VerticalContentAlignment()

.. autoclass:: webexpythonsdk.cards.options.Colors()

.. autoclass:: webexpythonsdk.cards.options.HorizontalAlignment()

.. autoclass:: webexpythonsdk.cards.options.FontSize()

.. autoclass:: webexpythonsdk.cards.options.FontWeight()

.. autoclass:: webexpythonsdk.cards.options.BlockElementHeight()

.. autoclass:: webexpythonsdk.cards.options.Spacing()

.. autoclass:: webexpythonsdk.cards.options.ImageSize()

.. autoclass:: webexpythonsdk.cards.options.ImageStyle()

.. autoclass:: webexpythonsdk.cards.options.ContainerStyle()

.. autoclass:: webexpythonsdk.cards.options.TextInputStyle()

.. autoclass:: webexpythonsdk.cards.options.ChoiceInputStyle()


Container
---------

.. autoclass:: webexpythonsdk.cards.container.Container()

.. autoclass:: webexpythonsdk.cards.container.ColumnSet()

.. autoclass:: webexpythonsdk.cards.container.FactSet()

.. autoclass:: webexpythonsdk.cards.container.ImageSet()

Inputs
------

.. autoclass:: webexpythonsdk.cards.inputs.Text()

.. autoclass:: webexpythonsdk.cards.inputs.Number()

.. autoclass:: webexpythonsdk.cards.inputs.Date()

.. autoclass:: webexpythonsdk.cards.inputs.Time()

.. autoclass:: webexpythonsdk.cards.inputs.Toggle()

.. autoclass:: webexpythonsdk.cards.inputs.Choices()

Actions
-------

.. autoclass:: webexpythonsdk.cards.actions.OpenUrl

.. autoclass:: webexpythonsdk.cards.actions.Submit

.. autoclass:: webexpythonsdk.cards.actions.ShowCard

*Copyright (c) 2016-2024 Cisco and/or its affiliates.*
