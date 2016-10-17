=============
ciscosparkapi
=============

----------------------------------------------------------------------------
Simple, lightweight and scalable Python API wrapper for the Cisco Spark APIs
----------------------------------------------------------------------------

Sure, working with the Cisco Spark APIs is easy (see `devloper.ciscospark.com`_).  They are RESTful, simply and naturally structured, require only a simple Access Token to authenticate, and the data is elegantly represented in intuitive JSON.  What could be easier?

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

Like I said, easy.  However, it is rather repetitive...

- You have to setup this same environment every time you want do something with just one of the API calls.
- ...and this was just posting a text message to Spark, what about when you want to do something like uploading a file?
- What if you your application or use case needs to make calls to several of the Spark APIs?
- This can turn into a lot of boiler plate code!
- Sure, you can consolidate the repetitious code into functions, and end up building your own library of functions (and many have done this!), or you can build upon the shoulders of those who have gone before you...

Enter **ciscosparkapi**, a simple API wrapper that wraps the RESTful Spark API calls and returned JSON objects within native Python objects and function calls.

The above Python code can be consolidated to the following:

.. code-block:: python
    from ciscosparkapi import CiscoSparkAPI

    api = CiscoSparkAPI()                                                  # Creates a new API 'connection object'
    try:
        message = api.messages.create('<room_id>', text='<message_text>')  # Creates a new message and raises an exception if something goes wrong.
        print("New message created, with ID:", message.id)
        print(message.text)
    except SparkApiError as e:                                             # Handles the exception, if something goes wrong
        print(e)

The ciscosparkapi package handles all of this for you:

+ Your Spark access token can automatically be retrieved from a ``SPARK_ACCESS_TOKEN`` environment variable.  *You don't have to provide it every time you create a new API connection object.*
+ *You don't have to remember the API endpoint URLs or JSON parameters.*  They have been wrapped in native Python methods.
+ If your Python IDE supports **auto-completion** (like PyCharm_), *you can simply navigate the available methods and object attributes right within your IDE*.
+ The JSON objects returned from the Cisco Spark cloud are modeled as native Python objects, which also support auto-completion and native attribute access.  *You don't have to think about parsing the JSON objects or working with dictionaries or creating lots of variables to hold the returned object's attributes.  You can simply interact with the returned object as a native Python object.*
+ When requesting 'lists of objects' from Spark, like enumerating the messages in a room or a list of rooms of which you are a member, you don't have think about handling and requesting pages_ of responses.  These are simply and efficiently abstracted and requested as needed - as you access the returned objects.  *Other than a slight delay as additional objects are requested from the Spark cloud, you won't have to deal with or think about pages of responses.*

...which lets you do powerful things simply:

.. code-block:: python
    from ciscosparkapi import CiscoSparkAPI

    api = CiscoSparkAPI()

    # Find all of rooms that have 'ciscosparkapi Demo' in their title
    all_rooms = api.rooms.list()
    demo_rooms = [room for room in all_rooms if 'ciscosparkapi Demo' in room.title]

    # Delete all of the demo rooms
    for room in demo_rooms:
        api.rooms.delete(room.id)

    # Create a new demo room
    demo_room = api.rooms.create('ciscosparkapi Demo')

    # Add people to the new demo room
    email_addresses = ["test01@cmlccie.com", "test02@cmlccie.com"]
    for email_address in email_addresses:
        api.memberships.create(demo_room.id, personEmail=email_address)

    # Post a message to the new room, and upload a file
    api.message.create(demo_room.id, text="Welcome to the room!", files=["welcome.jpg"])

That's at least six Spark API calls, and likely more than that depending on how rooms are returned by Spark (remember paging is handled for you automatically) and how many people you add to the room.  All in only about 23 lines (which includes comments).


Installation
------------

ciscosparkapi is available on PyPI.  Install it via PIP, or alternatively you can download the package from GitHub and install it via setuptools.

**PIP Installation**
.. code-block:: bash
    $ pip install ciscosparkapi

**git / setuptools Installation**
.. code-block:: bash
    $ git clone https://github.com/CiscoDevNet/ciscosparkapi.git
    $ python ciscosparkapi/setup.py install


Releases & Release Notes
------------------------

Complete and usable *Beta* releases have been published for this package.

While the package APIs may change while in beta, the package capabilities should all be functional.  If you expereince any issues using this package, please report them using the issues_ log on the packages GitHub page.

Please see the releases_ page for release notes on the incremental functionality and bug fixes that have been incorporated into the published releases.


Contribution
------------

ciscosparkapi_ and it's sister project ciscosparksdk_ are community development projects.  Feedback, thoughts, ideas and code contributions are most welcome!

To contribute to ciscosparkapi_ please use the following resources:
* Feedback, issues, thoughts and ideas... Please use the issues_ log.
* Interested in contributing code?
  # Check for open issues_ or create a new one.
    * Assign yourself to the issue you want to work on, and communicate with any others that may be working the issue.
    * Project workflow is being managed via the GitHub projects_ feature.  Move your issue to the 'In Progress' column of the project being worked.
  # Review the project charter_ for coding standards and practices.
  # Fork a copy of `the repository`_.
  # Add your code to your forked repository.
  # Submit a `pull request`_, and move your issue to the 'Code Review' column on the projects_ page.


.. _devloper.ciscospark.com: https://developer.ciscospark.com
.. _pages: https://developer.ciscospark.com/pagination.html
.. _PyCharm: https://www.jetbrains.com/pycharm/
.. _ciscosparkapi: https://github.com/CiscoDevNet/ciscosparkapi
.. _ciscosparksdk: https://github.com/CiscoDevNet/ciscosparksdk
.. _issues: https://github.com/CiscoDevNet/ciscosparkapi/issues
.. _projects: https://github.com/CiscoDevNet/ciscosparkapi/projects
.. _pull requests: https://github.com/CiscoDevNet/ciscosparkapi/pulls
.. _releases: https://github.com/CiscoDevNet/ciscosparkapi/releases
.. _charter: https://github.com/CiscoDevNet/spark-python-packages-team/blob/master/Charter.md
.. _the repository: ciscosparkapi_
.. _pull request: `pull requests`_
