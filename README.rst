=============
ciscosparkapi
=============

*Simple, lightweight, scalable Python API wrapper for the Cisco Spark APIs*

.. image:: https://img.shields.io/pypi/v/ciscosparkapi.svg
    :target: https://pypi.python.org/pypi/ciscosparkapi
.. image:: https://readthedocs.org/projects/ciscosparkapi/badge/?version=latest
    :target: http://ciscosparkapi.readthedocs.io/en/latest/?badge=latest

-------------------------------------------------------------------------------

**ciscosparkapi** is a *community developed* Pythonic wrapping of the Cisco
Spark APIs, which makes working with Cisco Spark in Python a *native* and
*natural* experience!

.. code-block:: python

    from ciscosparkapi import CiscoSparkAPI

    api = CiscoSparkAPI()

    # Find all rooms that have 'ciscosparkapi Demo' in their title
    all_rooms = api.rooms.list()
    demo_rooms = [room for room in all_rooms if 'ciscosparkapi Demo' in room.title]

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
    api.messages.create(demo_room.id, text="Welcome to the room!",
                        files=["https://developer.ciscospark.com/images/logo_spark_lg@256.png"])


That's more than 6 Spark API calls in less than 23 lines of code (with comments
and whitespace), and likely more than that since ciscosparkapi handles
pagination_ for you automatically!

ciscosparkapi makes your life better...  `Learn how!`__

__ Introduction_


Features
--------

ciscosparkapi does all of this for you...

+ Transparently sources your Spark credentials from your local environment

+ Provides and uses default arguments and settings everywhere possible, so you
  don't have to think about things like API endpoint URLs, HTTP headers and
  JSON formats

+ Represents all Cisco Spark API interactions using native Python tools

  + Authentication and Connection to the Cisco Spark Cloud ==>
    **CiscoSparkAPI** 'Connection Object'

  + API Calls ==> Hierarchically organized method calls underneath a
    **CiscoSparkAPI** 'Connection Object'

  + Returned Data Objects ==> Native Python objects

+ **Automatic and transparent pagination!**

+ Multipart encoding and uploading of local files

+ Auto-completion in your favorite IDE, descriptive exceptions, and so much
  more...


Installation
------------

Installing and upgrading ciscosparkapi is easy:

**Install via PIP**

.. code-block:: bash

    $ pip install ciscosparkapi

**Upgrading to the latest Version**

.. code-block:: bash

    $ pip install ciscosparkapi --upgrade


Documentation
-------------

**Excellent documentation is now available at:**
http://ciscosparkapi.readthedocs.io

Check out the Quickstart_ to dive in and begin using ciscosparkapi.


Examples
--------

Looking for some examples or sample scripts?  Check out the examples_ folder!

Have a good example script you would like to share?  Please feel free to
`contribute`__!

__ Contribution_


Release Notes
-------------

Complete and fully functional *Beta* releases have been published.  Please
see the releases_ page for release notes on the incremental functionality and
bug fixes incorporated into the published releases.

**Note:**  The package APIs may change, while the package is in beta.


Support
-------

This is a *community developed* and *community supported* project.  If you
experience any issues using this package, please report them using the
issues_ log.


Contribution
------------

ciscosparkapi_ and it's sister project ciscosparksdk_ are community
development projects.  Feedback, thoughts, ideas and code contributions are
most welcome!

**Feedback, issues, thoughts and ideas...**

Please use the issues_ log.

**Interested in contributing code?**

#. Check for open issues_ or create a new 'issue' for the item you want
   to work on.

   * Assign yourself to the issue, and communicate with any others that may be
     working the issue.

#. Review the project charter_ for coding standards and practices.
#. Fork a copy of `the repository`_.
#. Add your code to your forked repository.
#. Submit a `pull request`_.


*Copyright (c) 2016 Cisco Systems, Inc.*

.. _Introduction: http://ciscosparkapi.readthedocs.io/en/latest/user/intro.html
.. _pagination: https://developer.ciscospark.com/pagination.html
.. _ciscosparkapi.readthedocs.io: https://ciscosparkapi.readthedocs.io
.. _Quickstart: http://ciscosparkapi.readthedocs.io/en/latest/user/quickstart.html
.. _examples: https://github.com/CiscoDevNet/ciscosparkapi/tree/master/examples
.. _ciscosparkapi: https://github.com/CiscoDevNet/ciscosparkapi
.. _ciscosparksdk: https://github.com/CiscoDevNet/ciscosparksdk
.. _issues: https://github.com/CiscoDevNet/ciscosparkapi/issues
.. _projects: https://github.com/CiscoDevNet/ciscosparkapi/projects
.. _pull requests: https://github.com/CiscoDevNet/ciscosparkapi/pulls
.. _releases: https://github.com/CiscoDevNet/ciscosparkapi/releases
.. _charter: https://github.com/CiscoDevNet/spark-python-packages-team/blob/master/Charter.md
.. _the repository: ciscosparkapi_
.. _pull request: `pull requests`_
