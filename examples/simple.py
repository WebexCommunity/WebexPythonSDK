#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""Simple ciscosparkapi demonstration script.

Very simple script to create a demo room, post a message, and post a file.
If one or more rooms with the name of the demo room already exist, it will
delete the previously existing rooms.

The package natively retrieves your Spark access token from the
SPARK_ACCESS_TOKEN environment variable.  You must have this environment
variable set to run this script.

"""


from __future__ import print_function
from ciscosparkapi import CiscoSparkAPI


DEMO_ROOM_NAME = "ciscosparkapi Demo Room"
DEMO_PEOPLE = ["test01@cmlccie.com", "test02@cmlccie.com"]
DEMO_MESSAGE = u"Cisco Spark rocks!  \ud83d\ude0e"
DEMO_FILE_URL = "https://developer.ciscospark.com/images/logo_spark_lg@256.png"


api = CiscoSparkAPI()    # Create a CiscoSparkAPI connection object; uses your SPARK_ACCESS_TOKEN


# Clean up previous demo rooms
print("Searching for existing demo rooms...")
rooms = api.rooms.list()                                                          # Creates a generator container (iterable) that lists the rooms where you are a member
existing_demo_rooms = [room for room in rooms if room.title == DEMO_ROOM_NAME]    # Builds a list of rooms with the name DEMO_ROOM_NAME
if existing_demo_rooms:
    print("Found {} existing room(s); "
          "deleting them.".format(len(existing_demo_rooms)))
    for room in existing_demo_rooms:
         api.rooms.delete(room.id)                                                # Delete the room
         print ("Room '{}' deleted.".format(room.id))



demo_room = api.rooms.create(DEMO_ROOM_NAME)                          # Create a new demo room
print(demo_room)                                                      # Print the room details (formatted JSON)
for person_email in DEMO_PEOPLE:
    api.memberships.create(demo_room.id, personEmail=person_email)    # Add people to the room
message = api.messages.create(demo_room.id,text=DEMO_MESSAGE)         # Create a message in the new room
print(message)                                                        # Print the message details (formatted JSON)
message = api.messages.create(demo_room.id,files=[DEMO_FILE_URL])     # Post a file in the new room from test_url
print(message)                                                        # Print the message details (formatted JSON)
