.. _User API Doc:

.. currentmodule:: ciscosparkapi

============
User API Doc
============


Main Interface
==============

All of the API calls have been wrapped and hierarchically organized underneath
a single :class:`CiscoSparkAPI` class.

.. autoclass:: CiscoSparkAPI()
    :members:
    :exclude-members: access_token, base_url, timeout

    .. automethod:: CiscoSparkAPI.__init__


.. _people:

people
------

.. autoclass:: PeopleAPI()


.. _rooms:

rooms
-----

.. autoclass:: RoomsAPI()


.. _memberships:

memberships
-----------

.. autoclass:: MembershipsAPI()


.. _messages:

messages
--------

.. autoclass:: MessagesAPI()


.. _teams:

teams
-----

.. autoclass:: TeamsAPI()


.. _team_memberships:

team_memberships
----------------

.. autoclass:: TeamMembershipsAPI()


.. _webhooks:

webhooks
--------

.. autoclass:: WebhooksAPI()


.. _organizations:

organizations
-------------

.. autoclass:: OrganizationsAPI()


.. _licenses:

licenses
--------

.. autoclass:: LicensesAPI()


.. _roles:

roles
-----

.. autoclass:: RolesAPI()


.. _access_tokens:

access_tokens
-------------

.. autoclass:: AccessTokensAPI()


.. _Exceptions:

Exceptions
==========

.. autoexception:: ciscosparkapiException

.. autoexception:: SparkApiError

.. autoexception:: SparkRateLimitError


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
