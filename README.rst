==============
webexpythonsdk
==============

*Work with the Webex APIs in native Python!*

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/WebexCommunity/WebexPythonSDK/blob/master/LICENSE
    :alt: License MIT
.. image:: https://img.shields.io/pypi/v/webexpythonsdk
    :target: https://pypi.org/project/webexpythonsdk/
    :alt: PyPI Version
.. image:: https://img.shields.io/pypi/dw/webexpythonsdk?label=webexpythonsdk
    :target: https://pypistats.org/packages/webexpythonsdk
    :alt: webexpythonsdk PyPI Downloads
.. image:: https://img.shields.io/pypi/dw/webexteamssdk?label=webexteamssdk
    :target: https://pypistats.org/packages/webexteamssdk
    :alt: webexteamssdk PyPI Downloads
.. image:: https://img.shields.io/github/actions/workflow/status/WebexCommunity/WebexPythonSDK/.github%2Fworkflows%2Fbuild-and-test.yml?label=tests
    :target: https://github.com/WebexCommunity/WebexPythonSDK/actions/workflows/build-and-test.yml
    :alt: Tests Status
.. image:: https://img.shields.io/github/actions/workflow/status/WebexCommunity/WebexPythonSDK/.github%2Fworkflows%2Fdocs.yml?label=docs
    :target: https://webexcommunity.github.io/WebexPythonSDK/
    :alt: Documentation Status


---------------------------------------------------------------------------------------------------

Welcome to the new **webexpythonsdk** library! The latest release removes support for Python v2 and
is compatible with Python v3.10+. The new Webex Python SDK replaces the previous `webexteamssdk`_;
and with the exception of the Python version support and the name change, the two libraries are
functionally equivalent. The new library is the recommended choice for new projects, and
webexteamssdk users are encouraged to `migrate`_ to **webexpythonsdk**.

---------------------------------------------------------------------------------------------------


**webexpythonsdk** is a *community developed* Python library for working with the Webex APIs.  Our
goal is to make working with Webex in Python a *native* and *natural* experience!

.. code-block:: Python

    from webexpythonsdk import WebexAPI

    api = WebexAPI()

    # Find all rooms that have 'webexpythonsdk Demo' in their title
    all_rooms = api.rooms.list()
    demo_rooms = [room for room in all_rooms if 'webexpythonsdk Demo' in room.title]

    # Delete all of the demo rooms
    for room in demo_rooms:
        api.rooms.delete(room.id)

    # Create a new demo room
    demo_room = api.rooms.create('webexpythonsdk Demo')

    # Add people to the new demo room
    email_addresses = ["test01@cmlccie.com", "test02@cmlccie.com"]
    for email in email_addresses:
        api.memberships.create(demo_room.id, personEmail=email)

    # Post a message to the new room, and upload a file
    api.messages.create(demo_room.id, text="Welcome to the room!",
                        files=["https://www.webex.com/content/dam/wbx/us/images/navigation/CiscoWebex-Logo_white.png"])


That's more than 6 Webex API calls in less than 23 lines of code (with comments and whitespace),
and likely more than that, since webexpythonsdk handles pagination_ for you automatically!

webexpythonsdk makes your life better...  `Learn how!`__

__ Introduction_


Features
--------

webexpythonsdk does all of this for you:

* Transparently sources your Webex access token from your local environment

* Provides and uses default arguments and settings everywhere possible, so you don't have to think
  about things like API endpoint URLs, HTTP headers and JSON formats

* Represents all Webex API interactions using native Python tools

  * Authentication and Connection to the Webex Cloud ==> **WebexAPI** "connection object"

  * API Calls ==> Hierarchically organized methods underneath the **WebexAPI** 'Connection Object'

  * Returned Data Objects ==> Native Python objects

* **Automatic and transparent pagination!**

* **Automatic rate-limit handling!** *(wait|retry)*

* Multipart encoding and uploading of local files

* Auto-completion in your favorite IDE, descriptive exceptions, and so much more...


Installation
------------

Installing and upgrading webexpythonsdk is easy:

**Install via PIP**

.. code-block:: bash

    $ pip install webexpythonsdk

**Upgrade to the latest version**

.. code-block:: bash

    $ pip install webexpythonsdk --upgrade


Documentation
-------------

**Excellent documentation is now available at:**
https://webexcommunity.github.io/WebexPythonSDK

Check out the Quickstart_ to dive in and begin using webexpythonsdk.


Examples
--------

Are you looking for some sample scripts?  Check out the examples_ folder!

Have a good example script you would like to share?  Please feel free to `contribute`__!

__ Contribution_


Release Notes
-------------

Please see the releases_ page for release notes on the incremental functionality and bug fixes
incorporated into the published releases.


Questions, Support & Discussion
-------------------------------

webexpythonsdk is a *community developed* and *community-supported* project.  If you experience any
issues using this package, please report them using the issues_ page.

Please join the `Webex Python SDK - Python Community Contributors`__ Webex space to ask questions,
join the discussion, and share your projects and creations.

__ Community_


Contribution
------------

webexpythonsdk is a community development project.  Feedback, thoughts, ideas, and code
contributions are welcome! Please see the `Contributing`_ guide for more information.


History
-------

The Webex Python SDK (webexpythonsdk) library started as Cisco Spark API (ciscosparkapi) which
became Webex Teams SDK and then Webex Python SDK (webexpythonsdk). We updated the library's name in
alignment with Cisco's re-brand of Cisco Spark to Webex and then again to align the name with the
broader set of Webex APIs accessible via the SDK (meetings, recordings, etc.). The previous
versions of the library are deprecated and no longer supported; however, their open-source codebase
is still available in the `release/v0/ciscosparkapi`_ and `release/v1/webexteamssdk`_ branches in
this repository.

* `webexpythonsdk`_ (current) is compatible with Python v3.10+ and is the recommended library for
  new projects.

* `webexteamssdk`_ (deprecated) is compatible with Python v2 and v3 (<= v3.10) and is still
  available for existing projects. Users are encouraged to migrate to `webexpythonsdk`_.

* `ciscosparkapi`_ (deprecated) is compatible with Python v2 and v3 (<= v3.6) and should no longer
  be used.


*Copyright (c) 2016-2024 Cisco and/or its affiliates.*


.. _ciscosparkapi: https://github.com/WebexCommunity/WebexPythonSDK/tree/release/v0/ciscosparkapi
.. _Community: https://eurl.io/#BJ0A8gfOQ
.. _Contributing: https://github.com/WebexCommunity/WebexPythonSDK/blob/master/docs/contributing.rst
.. _examples: https://github.com/WebexCommunity/WebexPythonSDK/tree/master/examples
.. _Introduction: https://webexcommunity.github.io/WebexPythonSDK/user/intro.html
.. _issues: https://github.com/WebexCommunity/WebexPythonSDK/issues
.. _migrate: https://webexcommunity.github.io/WebexPythonSDK/user/migrate.html
.. _pagination: https://developer.webex.com/docs/basics#pagination
.. _projects: https://github.com/WebexCommunity/WebexPythonSDK/projects
.. _pull request: https://github.com/WebexCommunity/WebexPythonSDK/pulls
.. _pull requests: https://github.com/WebexCommunity/WebexPythonSDK/pulls
.. _Quickstart: https://webexcommunity.github.io/WebexPythonSDK/user/quickstart.html
.. _Release Plan: https://github.com/WebexCommunity/WebexPythonSDK/wiki/Release-Plans
.. _release/v0/ciscosparkapi: https://github.com/WebexCommunity/WebexPythonSDK/tree/release/v0/ciscosparkapi
.. _release/v1/webexteamssdk: https://github.com/WebexCommunity/WebexPythonSDK/tree/release/v1/webexteamssdk
.. _releases: https://github.com/WebexCommunity/WebexPythonSDK/releases
.. _the repository: https://github.com/WebexCommunity/WebexPythonSDK
.. _webexpythonsdk: https://github.com/WebexCommunity/WebexPythonSDK
.. _webexteamssdk: https://github.com/WebexCommunity/WebexPythonSDK/tree/release/v1/webexteamssdk
