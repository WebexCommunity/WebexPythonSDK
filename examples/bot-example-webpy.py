#!/usr/bin/env python2
#  -*- coding: utf-8 -*-
"""A simple bot script.

This sample script leverages web.py (see http://webpy.org/).  By default the
web server will be reachable at port 8080 - append a different port when
launching the script if desired.  ngrok can be used to tunnel traffic back to
your server if you don't wish to expose your machine publicly to the Internet.

You must create a Webex Teams webhook that points to the URL where this script
is hosted.  You can do this via the WebexTeamsAPI.webhooks.create() method.

Additional Webex Teams webhook details can be found here:
https://developer.webex.com/webhooks-explained.html

A bot must be created and pointed to this server in the My Apps section of
https://developer.webex.com.  The bot's Access Token should be added as a
'WEBEX_TEAMS_ACCESS_TOKEN' environment variable on the web server hosting this
script.

NOTE:  While this script is written to support Python versions 2 and 3, as of
the time of this writing web.py (v0.38) only supports Python 2.
Therefore this script only supports Python 2.

Copyright (c) 2016-2018 Cisco and/or its affiliates.

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


# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *


__author__ = "Brad Bester"
__author_email__ = "brbester@cisco.com"
__contributors__ = ["Chris Lunsford <chrlunsf@cisco.com>"]
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


import web
import requests

from webexteamssdk import WebexTeamsAPI, Webhook


# Module constants
CAT_FACTS_URL = 'https://catfact.ninja/fact'


# Global variables
# Your Webex Teams webhook should point to http://<serverip>:8080/events
urls = ('/events', 'webhook')
# Create the web application instance
app = web.application(urls, globals())
# Create the Webex Teams API connection object
api = WebexTeamsAPI()


def get_catfact():
    """Get a cat fact from catfact.ninja and return it as a string.

    Functions for Soundhound, Google, IBM Watson, or other APIs can be added
    to create the desired functionality into this bot.

    """
    response = requests.get(CAT_FACTS_URL, verify=False)
    response.raise_for_status()
    json_data = response.json()
    return json_data['fact']


class webhook(object):
    def POST(self):
        """Respond to inbound webhook JSON HTTP POSTs from Webex Teams."""
        # Get the POST data sent from Webex Teams
        json_data = web.data()
        print("\nWEBHOOK POST RECEIVED:")
        print(json_data, "\n")

        # Create a Webhook object from the JSON data
        webhook_obj = Webhook(json_data)
        # Get the room details
        room = api.rooms.get(webhook_obj.data.roomId)
        # Get the message details
        message = api.messages.get(webhook_obj.data.id)
        # Get the sender's details
        person = api.people.get(message.personId)

        print("NEW MESSAGE IN ROOM '{}'".format(room.title))
        print("FROM '{}'".format(person.displayName))
        print("MESSAGE '{}'\n".format(message.text))

        # This is a VERY IMPORTANT loop prevention control step.
        # If you respond to all messages...  You will respond to the messages
        # that the bot posts and thereby create a loop condition.
        me = api.people.me()
        if message.personId == me.id:
            # Message was sent by me (bot); do not respond.
            return 'OK'
        else:
            # Message was sent by someone else; parse message and respond.
            if "/CAT" in message.text:
                print("FOUND '/CAT'")
                # Get a cat fact
                cat_fact = get_catfact()
                print("SENDING CAT FACT '{}'".format(cat_fact))
                # Post the fact to the room where the request was received
                api.messages.create(room.id, text=cat_fact)
        return 'OK'


if __name__ == '__main__':
    # Start the web.py web server
    app.run()
