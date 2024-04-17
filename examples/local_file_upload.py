#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""Demo script showing how to upload a local file.

A simple script showing how to upload a local file when creating a message in
a Webex Teams space.

You upload a file by using the `files=` parameter of the
`WebexTeamsAPI.messages.create()` method, which expects to receive a list
containing a single string with the path to file to be attached to the created
message (Example: `files=["./image.png"]`).  The files parameter receives a
list to allow for future expansion; however today, only one file may be
included when creating a message via the Webex Teams APIs.

The WebexTeamsSDK natively retrieves your Webex Teams access token from the
WEBEX_TEAMS_ACCESS_TOKEN environment variable.  You must have this environment
variable set to run this script.


Copyright (c) 2016-2024 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import print_function

import os

from webexteamssdk import WebexTeamsAPI


__author__ = "Jeff Levensailor"
__author_email__ = "jeff@levensailor.com"
__contributors__ = ["Chris Lunsford <chrlunsf@cisco.com>"]
__copyright__ = "Copyright (c) 2016-2024 Cisco and/or its affiliates."
__license__ = "MIT"


ROOM_ID = "<your_room_id>"
FILE_PATH = "<the_path_to_the_local_file>"


# Create a WebexTeamsAPI connection object; uses your WEBEX_TEAMS_ACCESS_TOKEN
api = WebexTeamsAPI()


# Let's make sure the file exists
if not os.path.isfile(FILE_PATH):
    print("ERROR: File {} does not exist.".format(FILE_PATH))


# Not a requirement but to be completely clear let's make sure we are using
# an absolute path.
abs_path = os.path.abspath(FILE_PATH)


# The files parameter expects to receive a list containing a single string with
# the path to the file to be uploaded.
file_list = [abs_path]


# It takes just a single statement to upload the file and create the message
api.messages.create(roomId=ROOM_ID, files=file_list)
