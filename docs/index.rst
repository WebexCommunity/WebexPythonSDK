=============
ciscosparkapi
=============

-------------------------------------------------------------------------
Simple, lightweight, scalable Python API wrapper for the Cisco Spark APIs
-------------------------------------------------------------------------

Welcome to the docs!  ciscosparkapi is a *community developed* Pythonic
wrapping of the Cisco Spark APIs.  The package represents all of the Cisco
Spark API interactions via native Python tools.

===============================  ==============================================
Cisco Spark API                  ciscosparkapi Package
===============================  ==============================================
Authentication, URLs, & headers  Wrapped in a simple :class:`CiscoSparkAPI`
                                 "connection object"
-------------------------------  ----------------------------------------------
API Endpoints & Calls            Wrapped and represented as native method /
                                 function calls hierarchically structured
                                 underneath the :class:`CiscoSparkAPI`
                                 "connection object"
-------------------------------  ----------------------------------------------
Returned Spark Data Objects      Wrapped and represented as native Python
                                 objects
-------------------------------  ----------------------------------------------
Returned Lists of Objects        Wrapped and represented as iterable sequences
                                 that yield the native Spark Data Objects
===============================  ==============================================

This makes working with the Cisco Spark APIs in Python a *native* and *natural*
experience.  **ciscosparkapi helps you get things done faster.**  We'll take
care of the API semantics, and you can focus on writing your code.

.. code-block:: python

    from ciscosparkapi import CiscoSparkAPI

    # Create a new CiscoSparkAPI "connection object"
    api = CiscoSparkAPI()

    # Create an iterable object that represents all of my group rooms
    group_rooms = api.rooms.list(type='group')

    # Create a list of all rooms that have 'ciscosparkapi Demo' in their title
    demo_rooms = [room for room in group_rooms if 'ciscosparkapi Demo' in room.title]

    # Delete all of the demo rooms
    for room in demo_rooms:
        api.rooms.delete(room.id)

    # Create a new demo room
    demo_room = api.rooms.create('ciscosparkapi Demo')

    # Add people to the new demo room
    email_addresses = ["test01@cmlccie.com", "test02@cmlccie.com"]
    for email in email_addresses:
        api.memberships.create(demo_room.id, personEmail=email)

    # Post a message to the new room, and upload a file
    api.message.create(demo_room.id, text="Welcome to the room!", files=["welcome.jpg"])

With the ciscosparkapi package, you can easily:

* Interact with the Cisco Spark APIs in an interactive Python session *(like:
  finding the Spark ID for a room or a team, quickly getting a list of rooms
  that meet a criteria, ...)*

* Quickly create throw-away code that enables you get something done in Spark
  *(like: adding all of the members of one room/team to another room/team,
  exporting all of the messages in a room to a file, ...)*

* Leverage the API wrapper to cleanly add Spark functionality to your project
  without having to write the boilerplate code for working with the Spark APIs


Getting Started
===============

Install the ciscosparkapi package using ``pip``, and then check out the :ref:`Tutorial` page
to get started.

**Installation via PIP**

.. code-block:: bash

    $ pip install ciscosparkapi


General Information about the Cisco Spark Service
=================================================

What is Cisco Spark?
--------------------

    "Cisco Spark is where all your work lives.  Bring your teams together in a
     place that makes it easy to keep people and work connected."

Check out the official `Cisco Spark`_ website for more information and to
create a free account!

Spark for Developers
--------------------

Leveraging the Cisco Spark APIs and developing on top of the Cisco Spark cloud
is easy.  Signup for a `free account`_ and then head over to the
`Spark for Developers`_ website.


User Guides
===========

.. toctree::
    :maxdepth: 2

    user/intro
    user/tutorial
    user/api


Developer Guides
================

Developer docs are *coming soon*.  For now, please see the contribution_
instructions on the ciscosparkapi_ GitHub page to get started.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


*Copyright (c) 2016 Cisco Systems, Inc.*

.. _free account: `Cisco Spark`
.. _Cisco Spark: https://www.ciscospark.com/
.. _Spark for Developers: https://developer.ciscospark.com/
.. _contribution: https://github.com/CiscoDevNet/ciscosparkapi#contribution
.. _ciscosparkapi: https://github.com/CiscoDevNet/ciscosparkapi
