.. _Introduction:

============
Introduction
============


Work with the Webex Teams APIs in Native Python!
------------------------------------------------

Sure, working with the Webex Teams APIs is easy (see
`developer.webex.com`_).  They are RESTful,  naturally structured,
require only a simple Access Token for authentication, and the data is
elegantly represented in intuitive JSON.  What could be easier?

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
        message_text = response.json['text']
        print("New message created, with ID:", message_id)
        print(message_text)
    else:
        # Oops something went wrong...  Better do something about it.
        print(response.status_code, response.text)

Like I said, EASY.  However, in use, the code can become rather repetitive...

- You have to setup the environment every time
- You have to remember URLs, request parameters and JSON formats
  (or reference the docs)
- You have to parse the returned JSON and work with multiple layers of list
  and dictionary indexes
- When requesting lists of items, you have to deal with pagination_


Enter **webexteamssdk**, a simple API wrapper that wraps all of the Webex Teams API
calls and returned JSON objects within native Python objects and methods.

With webexteamssdk, the above Python code can be consolidated to the following:

.. code-block:: python

    from webexteamssdk import WebexTeamsAPI

    api = WebexTeamsAPI()
    try:
        message = api.messages.create('<room_id>', text='<message_text>')
        print("New message created, with ID:", message.id)
        print(message.text)
    except ApiError as e:
        print(e)


**webexteamssdk handles all of this for you:**

+ Reads your Webex Teams access token from a ``WEBEX_TEAMS_ACCESS_TOKEN`` environment
  variable

+ Wraps and represents all Webex Teams API calls as a simple hierarchical tree of
  native-Python methods (with default arguments provided everywhere possible!)

+ If your Python IDE supports **auto-completion** (like PyCharm_), you can
  navigate the available methods and object attributes right within your IDE

+ Represents all returned JSON objects as native Python objects - you can
  access all of the object's attributes using native *dot.syntax*

+ **Automatic and Transparent Pagination!**  When requesting 'lists of objects'
  from Webex Teams, requests for additional pages of responses are efficiently and
  automatically requested as needed

+ **Automatic Rate-Limit Handling**  Sending a lot of requests to Webex Teams?
  Don't worry; we have you covered.  Webex Teams will respond with a rate-limit
  response, which will automatically be caught and "handled" for you.  Your
  requests and script will automatically be "paused" for the amount of time
  specified by Webex Teams, while we wait for the Webex Teams rate-limit timer to cool
  down.  After the cool-down, your request will automatically be retried, and
  your script will continue to run as normal.  Handling all of this requires
  zero (0) changes to your code - you're welcome.  😎

  Just know that if you are are sending a lot of requests, your script might
  take longer to run if your requests are getting rate limited.

+ Multipart encoding and uploading of local files, when creating messages with
  local file attachments


All of this, combined, lets you do powerful things simply:

.. code-block:: python

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


That's more than 6 Webex Teams API calls in less than 23 lines of code (with comments
and whitespace), and likely more than that since webexteamssdk handles
pagination_ for you automatically!

Head over to the :ref:`Quickstart` page to begin working with the
**Webex Teams APIs in native Python**!


.. _MITLicense:

MIT License
-----------

webexteamssdk is currently licensed under the `MIT Open Source License`_, and
distributed as a source distribution (no binaries) via :ref:`PyPI <Install>`,
and the complete :ref:`source code <Source Code>` is available on GitHub.

webexteamssdk License
---------------------

.. include:: ../../LICENSE


*Copyright (c) 2016-2018 Cisco and/or its affiliates.*


.. _MIT Open Source License: https://opensource.org/licenses/MIT
.. _developer.webex.com: https://developer.webex.com
.. _pagination: https://developer.webex.com/pagination.html
.. _PyCharm: https://www.jetbrains.com/pycharm/

