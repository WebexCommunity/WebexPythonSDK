.. _User API Doc:

.. currentmodule:: ciscosparkapi

============
User API Doc
============


CiscoSparkAPI
=============

The :class:`CiscoSparkAPI` class is the main interface for the package. All of
the Spark APIs (people, rooms, etc.) and their API endpoints have been wrapped
and hierarchically organized underneath the :class:`CiscoSparkAPI` class.

.. autoclass:: CiscoSparkAPI()
    :members:
    :exclude-members: access_token, base_url, timeout

    .. automethod:: CiscoSparkAPI.__init__


.. _people:

people
------

.. autoclass:: ciscosparkapi.api.people.PeopleAPI()


.. _rooms:

rooms
-----

.. autoclass:: ciscosparkapi.api.rooms.RoomsAPI()


.. _memberships:

memberships
-----------

.. autoclass:: ciscosparkapi.api.memberships.MembershipsAPI()


.. _messages:

messages
--------

.. autoclass:: ciscosparkapi.api.messages.MessagesAPI()


.. _teams:

teams
-----

.. autoclass:: ciscosparkapi.api.teams.TeamsAPI()


.. _team_memberships:

team_memberships
----------------

.. autoclass:: ciscosparkapi.api.team_memberships.TeamMembershipsAPI()


.. _webhooks:

webhooks
--------

.. autoclass:: ciscosparkapi.api.webhooks.WebhooksAPI()


.. _organizations:

organizations
-------------

.. autoclass:: ciscosparkapi.api.organizations.OrganizationsAPI()


.. _licenses:

licenses
--------

.. autoclass:: ciscosparkapi.api.licenses.LicensesAPI()


.. _roles:

roles
-----

.. autoclass:: ciscosparkapi.api.roles.RolesAPI()


.. _events:

events
-----

.. autoclass:: ciscosparkapi.api.events.EventsAPI()


.. _access_tokens:

access_tokens
-------------

.. autoclass:: ciscosparkapi.api.access_tokens.AccessTokensAPI()


.. _Exceptions:

Exceptions
==========

.. autoexception:: ciscosparkapiException()
    :show-inheritance:
    :members:

.. autoexception:: SparkApiError()
    :show-inheritance:
    :members:

.. autoexception:: SparkRateLimitError()
    :show-inheritance:
    :members:


.. _Spark Data Objects:

Spark Data Objects
==================


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


*Copyright (c) 2016-2018 Cisco and/or its affiliates.*
