=============
webexpythonsdk
=============

*Work with the Webex APIs in native Python!*

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/WebexCommunity/WebexPythonSDK/blob/master/LICENSE
.. image:: https://img.shields.io/pypi/v/webexpythonsdk.svg
    :target: https://pypi.org/project/webexpythonsdk/
.. image:: https://img.shields.io/pypi/dw/webexpythonsdk.svg
    :target: https://pypi.org/project/webexpythonsdk/
.. image:: https://readthedocs.org/projects/webexpythonsdk/badge/?version=latest
    :target: http://webexpythonsdk.readthedocs.io/en/latest/?badge=latest

------------------------------------------------------------------------------------------------------------------------


**webexpythonsdk** v1.7 will be the last 🤞 release of the `webexpythonsdk` package. This will be the last release
supporting Python v2 and v3 compatibility; it is compatible Python v3 releases *up to Python v3.10*.

Going forward, the `webexpythonsdk` package will be replaced by the `WebexPythonSDK` package, which will support Python
v3.10+.

------------------------------------------------------------------------------------------------------------------------


**webexpythonsdk** is a *community developed* Python library for working with the Webex APIs.  Our goal is to make
working with Webex in Python a *native* and *natural* experience!

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


That's more than 6 Webex API calls in less than 23 lines of code (with comments and whitespace), and likely more
than that, since webexpythonsdk handles pagination_ for you automatically!

webexpythonsdk makes your life better...  `Learn how!`__

__ Introduction_


Features
--------

webexpythonsdk does all of this for you:

* Transparently sources your Webex access token from your local environment

* Provides and uses default arguments and settings everywhere possible, so you don't have to think about things like API
  endpoint URLs, HTTP headers and JSON formats

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
http://webexpythonsdk.readthedocs.io

Check out the Quickstart_ to dive in and begin using webexpythonsdk.


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

webexpythonsdk is a *community developed* and *community-supported* project.  If you experience any issues using this
package, please report them using the issues_ page.

Please join the `Python Webex Devs`__ Webex space to ask questions, join the discussion, and share your
projects and creations.

__ Community_


Contribution
------------

webexpythonsdk is a community development project.  Feedback, thoughts, ideas, and code contributions are welcome!
Please see the `Contributing`_ guide for more information.


History
-------

The Webex Python SDK (webexpythonsdk) library started as Cisco Spark API (ciscosparkapi). We updated the library's name in
alignment with Cisco's re-brand of Cisco Spark to Webex. The Cisco Spark API library has been deprecated and is no
longer supported; however, its open-source codebase is still available in the `ciscosparkapi`_ branch of this
repository.

The development team may make additional name changes as the library evolves with the Webex APIs published on
developer.webex.com.


*Copyright (c) 2016-2024 Cisco and/or its affiliates.*


.. _Release Plan: https://github.com/WebexCommunity/WebexPythonSDK/wiki/Release-Plans
.. _Introduction: http://webexpythonsdk.readthedocs.io/en/latest/user/intro.html
.. _pagination: https://developer.webex.com/docs/basics#pagination
.. _webexpythonsdk.readthedocs.io: https://webexpythonsdk.readthedocs.io
.. _Quickstart: http://webexpythonsdk.readthedocs.io/en/latest/user/quickstart.html
.. _examples: https://github.com/WebexCommunity/WebexPythonSDK/tree/master/examples
.. _webexpythonsdk: https://github.com/WebexCommunity/WebexPythonSDK
.. _issues: https://github.com/WebexCommunity/WebexPythonSDK/issues
.. _Community: https://eurl.io/#HkMxO-_9-
.. _projects: https://github.com/WebexCommunity/WebexPythonSDK/projects
.. _pull requests: https://github.com/WebexCommunity/WebexPythonSDK/pulls
.. _releases: https://github.com/WebexCommunity/WebexPythonSDK/releases
.. _the repository: webexpythonsdk_
.. _pull request: `pull requests`_
.. _Contributing: https://github.com/WebexCommunity/WebexPythonSDK/blob/master/docs/contributing.rst
.. _ciscosparkapi: https://github.com/CiscoDevNet/ciscosparkapi/tree/ciscosparkapi
