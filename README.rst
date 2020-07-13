=============
webexteamssdk
=============

*Work with the Webex Teams APIs in native Python!*

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/CiscoDevNet/webexteamssdk/blob/master/LICENSE
.. image:: https://img.shields.io/pypi/v/webexteamssdk.svg
    :target: https://pypi.org/project/webexteamssdk/
.. image:: https://img.shields.io/pypi/dw/webexteamssdk.svg
    :target: https://pypi.org/project/webexteamssdk/
.. image:: https://travis-ci.org/CiscoDevNet/webexteamssdk.svg?branch=master
    :target: https://travis-ci.org/CiscoDevNet/webexteamssdk
.. image:: https://readthedocs.org/projects/webexteamssdk/badge/?version=latest
    :target: http://webexteamssdk.readthedocs.io/en/latest/?badge=latest

------------------------------------------------------------------------------------------------------------------------


With release v1.6 we are wrapping up active development on the v1.x release and shifting our focus to the next major
release v2!  Please see the work-in-progress `Release Plan`_ and contribute your ideas for v2.x enhancements by either
opening enhancement issues_ or by joining our
`webexteamssdk - Webex Teams SDK - Python Community Contributors <https://eurl.io/#BJ0A8gfOQ>`_ space and posting your
ideas there.

------------------------------------------------------------------------------------------------------------------------


**webexteamssdk** is a *community developed* Python library for working with the Webex Teams APIs.  Our goal is to make
working with Webex Teams in Python a *native* and *natural* experience!

.. code-block:: Python

    from webexteamssdk import WebexTeamsAPI

    api = WebexTeamsAPI()

    # Find all rooms that have 'webexteamssdk Demo' in their title
    all_rooms = api.rooms.list()
    demo_rooms = [room for room in all_rooms if 'webexteamssdk Demo' in room.title]

    # Delete all of the demo rooms
    for room in demo_rooms:
        api.rooms.delete(room.id)

    # Create a new demo room
    demo_room = api.rooms.create('webexteamssdk Demo')

    # Add people to the new demo room
    email_addresses = ["test01@cmlccie.com", "test02@cmlccie.com"]
    for email in email_addresses:
        api.memberships.create(demo_room.id, personEmail=email)

    # Post a message to the new room, and upload a file
    api.messages.create(demo_room.id, text="Welcome to the room!",
                        files=["https://www.webex.com/content/dam/wbx/us/images/dg-integ/teams_icon.png"])


That's more than 6 Webex Teams API calls in less than 23 lines of code (with comments and whitespace), and likely more
than that, since webexteamssdk handles pagination_ for you automatically!

webexteamssdk makes your life better...  `Learn how!`__

__ Introduction_


Features
--------

webexteamssdk does all of this for you:

* Transparently sources your Webex Teams access token from your local environment

* Provides and uses default arguments and settings everywhere possible, so you don't have to think about things like API
  endpoint URLs, HTTP headers and JSON formats

* Represents all Webex Teams API interactions using native Python tools

  * Authentication and Connection to the Webex Teams Cloud ==> **WebexTeamsAPI** "connection object"

  * API Calls ==> Hierarchically organized methods underneath the **WebexTeamsAPI** 'Connection Object'

  * Returned Data Objects ==> Native Python objects

* **Automatic and transparent pagination!**

* **Automatic rate-limit handling!** *(wait|retry)*

* Multipart encoding and uploading of local files

* Auto-completion in your favorite IDE, descriptive exceptions, and so much more...


Installation
------------

Installing and upgrading webexteamssdk is easy:

**Install via PIP**

.. code-block:: bash

    $ pip install webexteamssdk

**Upgrade to the latest version**

.. code-block:: bash

    $ pip install webexteamssdk --upgrade


Documentation
-------------

**Excellent documentation is now available at:**
http://webexteamssdk.readthedocs.io

Check out the Quickstart_ to dive in and begin using webexteamssdk.


Examples
--------

Are you looking for some sample scripts?  Check out the examples_ folder!

Have a good example script you would like to share?  Please feel free to `contribute`__!

__ Contribution_


Release Notes
-------------

Please see the releases_ page for release notes on the incremental functionality and bug fixes incorporated into the
published releases.


Questions, Support & Discussion
-------------------------------

webexteamssdk is a *community developed* and *community-supported* project.  If you experience any issues using this
package, please report them using the issues_ page.

Please join the `Python Webex Teams Devs`__ Webex Teams space to ask questions, join the discussion, and share your
projects and creations.

__ Community_


Contribution
------------

webexteamssdk_ is a community development project.  Feedback, thoughts, ideas, and code contributions are welcome!
Please see the `Contributing`_ guide for more information.


History
-------

The Webex Teams SDK (webexteamssdk) library started as Cisco Spark API (ciscosparkapi). We updated the library's name in
alignment with Cisco's re-brand of Cisco Spark to Webex Teams. The Cisco Spark API library has been deprecated and is no
longer supported; however, its open-source codebase is still available in the `ciscosparkapi`_ branch of this
repository.

The development team may make additional name changes as the library evolves with the Webex APIs published on
developer.webex.com.


*Copyright (c) 2016-2020 Cisco and/or its affiliates.*


.. _Release Plan: https://github.com/CiscoDevNet/webexteamssdk/wiki/Release-Plans
.. _Introduction: http://webexteamssdk.readthedocs.io/en/latest/user/intro.html
.. _pagination: https://developer.webex.com/pagination.html
.. _webexteamssdk.readthedocs.io: https://webexteamssdk.readthedocs.io
.. _Quickstart: http://webexteamssdk.readthedocs.io/en/latest/user/quickstart.html
.. _examples: https://github.com/CiscoDevNet/webexteamssdk/tree/master/examples
.. _webexteamssdk: https://github.com/CiscoDevNet/webexteamssdk
.. _issues: https://github.com/CiscoDevNet/webexteamssdk/issues
.. _Community: https://eurl.io/#HkMxO-_9-
.. _projects: https://github.com/CiscoDevNet/webexteamssdk/projects
.. _pull requests: https://github.com/CiscoDevNet/webexteamssdk/pulls
.. _releases: https://github.com/CiscoDevNet/webexteamssdk/releases
.. _the repository: webexteamssdk_
.. _pull request: `pull requests`_
.. _Contributing: https://github.com/CiscoDevNet/webexteamssdk/blob/master/docs/contributing.rst
.. _ciscosparkapi: https://github.com/CiscoDevNet/ciscosparkapi/tree/ciscosparkapi
