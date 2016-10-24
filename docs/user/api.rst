============================================
ciscosparkapi Package User-API Documentation
============================================


Main Interface
==============

.. module:: ciscosparkapi

All of the API calls have been wrapped and hierarchally organized underneath a
single ``CiscoSparkAPI`` class.

.. autoclass:: CiscoSparkAPI()
    :members:
    :exclude-members: access_token, base_url, timeout

    .. automethod:: CiscoSparkAPI.__init__


People API
----------

.. autoclass:: PeopleAPI()


Rooms API
---------

.. autoclass:: RoomsAPI()


Memberships API
---------------

.. autoclass:: MembershipsAPI()


Messages API
------------

.. autoclass:: MessagesAPI()


Teams API
---------

.. autoclass:: TeamsAPI()


Team Memberships API
--------------------

.. autoclass:: TeamMembershipsAPI()


Webhooks API
------------

.. autoclass:: WebhooksAPI()


Access Tokens API
-----------------

.. autoclass:: AccessTokensAPI()


Exceptions
==========

.. autoexception:: ciscosparkapiException

.. autoexception:: SparkApiError


Spark Data Objects
==================

Person
------

.. autoclass:: Person()


Room
----

.. autoclass:: Room()


Membership
----------

.. autoclass:: Membership()


Message
-------

.. autoclass:: Message()


Team
----

.. autoclass:: Team()


Team Membership
---------------

.. autoclass:: TeamMembership()


Webhooks
--------

.. autoclass:: Webhook()


Access Token
------------

.. autoclass:: AccessToken()
