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


.. _access_tokens:

access_tokens
-------------

.. autoclass:: webexteamssdk.api.access_tokens.AccessTokensAPI()


.. _admin_audit_events:

admin_audit_events
------------------

.. autoclass:: webexteamssdk.api.admin_audit_events.AdminAuditEventsAPI()


.. _attachment_actions:

attachment_actions
------------------

.. autoclass:: webexteamssdk.api.attachment_actions.AttachmentActionsAPI()


.. _events:

events
------

.. autoclass:: webexteamssdk.api.events.EventsAPI()


.. _guest_issuer:

guest_issuer
------------

.. autoclass:: webexteamssdk.api.guest_issuer.GuestIssuerAPI()


.. _licenses:

licenses
--------

.. autoclass:: webexteamssdk.api.licenses.LicensesAPI()


.. _memberships:

memberships
-----------

.. autoclass:: webexteamssdk.api.memberships.MembershipsAPI()


.. _messages:

messages
--------

.. autoclass:: webexteamssdk.api.messages.MessagesAPI()


.. _organizations:

organizations
-------------

.. autoclass:: webexteamssdk.api.organizations.OrganizationsAPI()


.. _people:

people
------

.. autoclass:: webexteamssdk.api.people.PeopleAPI()


.. _roles:

roles
-----

.. autoclass:: webexteamssdk.api.roles.RolesAPI()


.. _rooms:

rooms
-----

.. autoclass:: webexteamssdk.api.rooms.RoomsAPI()


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


.. _Webex Teams Data Objects:

Webex Teams Data Objects
========================


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

.. autoexception:: webexteamssdkWarning()
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

.. autoclass:: webexteamssdk.cards.card.AdaptiveCard()

Components
----------

.. autoclass:: webexteamssdk.cards.components.Image()
   :members:

   .. automethod:: __init__

.. autoclass:: webexteamssdk.cards.components.TextBlock()
   :members:

   .. automethod:: __init__

.. autoclass:: webexteamssdk.cards.components.Column()

.. autoclass:: webexteamssdk.cards.components.Fact()

.. autoclass:: webexteamssdk.cards.components.Choice()

Options
-------

.. autoclass:: webexteamssdk.cards.options.VerticalContentAlignment()

.. autoclass:: webexteamssdk.cards.options.Colors()

.. autoclass:: webexteamssdk.cards.options.HorizontalAlignment()

.. autoclass:: webexteamssdk.cards.options.FontSize()

.. autoclass:: webexteamssdk.cards.options.FontWeight()

.. autoclass:: webexteamssdk.cards.options.BlockElementHeight()

.. autoclass:: webexteamssdk.cards.options.Spacing()

.. autoclass:: webexteamssdk.cards.options.ImageSize()

.. autoclass:: webexteamssdk.cards.options.ImageStyle()

.. autoclass:: webexteamssdk.cards.options.ContainerStyle()

.. autoclass:: webexteamssdk.cards.options.TextInputStyle()

.. autoclass:: webexteamssdk.cards.options.ChoiceInputStyle()


Container
---------

.. autoclass:: webexteamssdk.cards.container.Container()

.. autoclass:: webexteamssdk.cards.container.ColumnSet()

.. autoclass:: webexteamssdk.cards.container.FactSet()

.. autoclass:: webexteamssdk.cards.container.ImageSet()

Inputs
------

.. autoclass:: webexteamssdk.cards.inputs.Text()

.. autoclass:: webexteamssdk.cards.inputs.Number()

.. autoclass:: webexteamssdk.cards.inputs.Date()

.. autoclass:: webexteamssdk.cards.inputs.Time()

.. autoclass:: webexteamssdk.cards.inputs.Toggle()

.. autoclass:: webexteamssdk.cards.inputs.Choices()

Actions
-------

.. autoclass:: webexteamssdk.cards.actions.OpenUrl

.. autoclass:: webexteamssdk.cards.actions.Submit

.. autoclass:: webexteamssdk.cards.actions.ShowCard

*Copyright (c) 2016-2024 Cisco and/or its affiliates.*
