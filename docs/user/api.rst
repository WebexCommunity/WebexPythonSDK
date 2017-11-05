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


.. _Room:

Room
----

.. autoclass:: Room()


.. _Membership:

Membership
----------

.. autoclass:: Membership()


.. _Message:

Message
-------

.. autoclass:: Message()


.. _Team:

Team
----

.. autoclass:: Team()


.. _Team Membership:

Team Membership
---------------

.. autoclass:: TeamMembership()


.. _Webhook:

Webhook
-------

.. autoclass:: Webhook()


.. _WebhookEvent:

Webhook Event
-------------

.. autoclass:: WebhookEvent()


.. _Organization:

Organization
------------

.. autoclass:: Organization()


.. _License:

License
-------

.. autoclass:: License()


.. _Role:

Role
----

.. autoclass:: Role()


.. _Access Token:

Access Token
------------

.. autoclass:: AccessToken()


*Copyright (c) 2016 Cisco Systems, Inc.*
