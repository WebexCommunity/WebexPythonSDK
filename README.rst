=============
ciscosparkapi
=============

-------------------------------------------------------------------------
Simple, lightweight, scalable Python API wrapper for the Cisco Spark APIs
-------------------------------------------------------------------------

.. image:: https://img.shields.io/pypi/v/ciscosparkapi.svg
    :target: https://pypi.python.org/pypi/ciscosparkapi

Sure, working with the Cisco Spark APIs is easy (see `developer.ciscospark.com`_).  They are *RESTful*,  *naturally structured*, require only a *simple Access Token for authentication*, and *the data is elegantly represented in intuitive JSON*.  What could be easier?

.. code-block:: python

    import requests

    URL = 'https://api.ciscospark.com/v1/messages'
    ACCESS_TOKEN = '<your_access_token>'
    ROOM_ID = '<room_id>'
    MESSAGE_TEXT = '<message_text>'

    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,
               'Content-type': 'application/json;charset=utf-8'}
    post_data = {'roomId': ROOM_ID,
                 'text': MESSAGE_TEXT}
    response = requests.post(URL, json=post_data, headers=headers)
    if response.status_code == 200:
        # Great your message was posted!
        message_id = response.json['id']
        message_text = response.json['id']
        print("New message created, with ID:", message_id)
        print(message_text)
    else:
        # Oops something went wrong...  Better do something about it.
        print(response.status_code, response.text)

Like I said, *EASY*.  However, in use, the code can be rather repetitive...

- You have to setup the environment every time
- You have to remember URLs and request arguments (or reference the docs)
- You have to parse the returned JSON and setup variables to hold the attributes you need
- When requesting lists of items, you have to deal with pagination_


Enter **ciscosparkapi**, a simple API wrapper that wraps all of the Spark API calls and returned JSON objects within native Python objects and function calls.

With ciscosparkapi, the above Python code can be consolidated to the following:

.. code-block:: python

    from ciscosparkapi import CiscoSparkAPI

    api = CiscoSparkAPI()
    try:
        message = api.messages.create('<room_id>', text='<message_text>')
        print("New message created, with ID:", message.id)
        print(message.text)
    except SparkApiError as e:
        print(e)

The ciscosparkapi package handles all of this for you:

+ Reads your Spark access token from a ``SPARK_ACCESS_TOKEN`` environment variable
+ Wraps and represents all Spark API calls as a simple hierarchical tree of native-Python methods (with default arguments provided everywhere possible!)
+ If your Python IDE supports **auto-completion** (like PyCharm_), you can navigate the available methods and object attributes right within your IDE
+ Represents all returned JSON objects as native Python objects - you can access all of the object's attributes using native *dot.syntax*
+ **Automatic and Transparent Pagination!**  When requesting 'lists of objects' from Spark, requests for additional pages of responses are efficiently and automatically requested as needed
+ Multipart encoding and uploading of local files, when creating messages with local file attachments

All of this, combined, lets you do powerful things simply:

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
    api.message.create(demo_room.id, text="Welcome to the room!", files=["welcome.jpg"])

That's more than six Spark API calls in less than 23 lines of script code (with comments)!
...and likely more than that depending on how many rooms are returned by Spark (remember pagination is handled for you automatically)


Installation
------------

Installation and updating of ciscosparkapi is easy:

**Install via PIP**

.. code-block:: bash

    $ pip install ciscosparkapi

**Upgrading to the latest Version**

.. code-block:: bash

    $ pip install ciscosparkapi --upgrade


Releases & Release Notes
------------------------

Complete and usable *Beta* releases_ have been published for this package.

While the package APIs may change (while the package is in beta), the package capabilities should all be functional.  If you experience any issues using this package, please report them using the issues_ log.

Please see the releases_ page for release notes on the incremental functionality and bug fixes that have been incorporated into the published releases.


Examples
--------

Looking for some examples or sample scripts?  Check out the examples_ folder!

Have a good example script you would like to share?  Please feel free to contribute!


Documentation
-------------

All of the user-facing methods have complete docstrings.  You can view the docstrings for any method either from the `source files`_, or by using the Python ``help()`` function.

.. code-block:: python

    >>> from ciscosparkapi import CiscoSparkAPI
    >>> api = CiscoSparkAPI()
    >>> help(api.messages.create)
    create(self, roomId=None, toPersonId=None, toPersonEmail=None, text=None, markdown=None, files=None) method of ciscosparkapi.api.messages.MessagesAPI instance
        Posts a message to a room.

        Posts a message, and optionally, a media content attachment, to a room.

        You must specify either a roomId, toPersonId or toPersonEmail when
        posting a message, and you must supply some message content (text,
        markdown, files).

        Args:
            roomId(string_types): The room ID.
            toPersonId(string_types): The ID of the recipient when sending a
                private 1:1 message.
     ...

Full standalone online documentation is coming soon (it's on the backlog!).


Contribution
------------

ciscosparkapi_ and it's sister project ciscosparksdk_ are community development projects.  Feedback, thoughts, ideas and code contributions are most welcome!

To contribute to ciscosparkapi please use the following resources:

Feedback, issues, thoughts and ideas... Please use the issues_ log.

Interested in contributing code?

#. Check for open issues_ or create a new one.

   * Assign yourself to the issue you want to work on, and communicate with any others that may be working the issue.
   * Project workflow is being managed via the GitHub projects_ feature.  Move your issue to the 'In Progress' column of the project being worked.

#. Review the project charter_ for coding standards and practices.
#. Fork a copy of `the repository`_.
#. Add your code to your forked repository.
#. Submit a `pull request`_, and move your issue to the 'Code Review' column on the projects_ page.


.. _developer.ciscospark.com: https://developer.ciscospark.com
.. _pagination: https://developer.ciscospark.com/pagination.html
.. _PyCharm: https://www.jetbrains.com/pycharm/
.. _examples: https://github.com/CiscoDevNet/ciscosparkapi/tree/master/examples
.. _source files: https://github.com/CiscoDevNet/ciscosparkapi/tree/master/ciscosparkapi
.. _ciscosparkapi: https://github.com/CiscoDevNet/ciscosparkapi
.. _ciscosparksdk: https://github.com/CiscoDevNet/ciscosparksdk
.. _issues: https://github.com/CiscoDevNet/ciscosparkapi/issues
.. _projects: https://github.com/CiscoDevNet/ciscosparkapi/projects
.. _pull requests: https://github.com/CiscoDevNet/ciscosparkapi/pulls
.. _releases: https://github.com/CiscoDevNet/ciscosparkapi/releases
.. _charter: https://github.com/CiscoDevNet/spark-python-packages-team/blob/master/Charter.md
.. _the repository: ciscosparkapi_
.. _pull request: `pull requests`_
