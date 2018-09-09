#  -*- coding: utf-8 -*-
"""A simple bot script, built on Pyramid using Cornice.

This sample script leverages the Pyramid web framework https://trypyramid.com/
with Cornice https://cornice.readthedocs.io.  By default the web server will be
reachable at port 6543 you can change this default if desired
(see `pyramidWebexTeamsBot.ini`).

ngrok (https://ngrok.com/) can be used to tunnel traffic back to your server
if your machine sits behind a firewall.

You must create a Webex Teams webhook that points to the URL where this script
is hosted.  You can do this via the WebexTeamsAPI.webhooks.create() method.

Additional Webex Teams webhook details can be found here:
https://developer.webex.com/webhooks-explained.html

A bot must be created and pointed to this server in the My Apps section of
https://developer.webex.com.  The bot's Access Token should be added as a
'WEBEX_TEAMS_ACCESS_TOKEN' environment variable on the web server hosting this
script.

This script supports Python versions 2 and 3.

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


__author__ = "Jose Bogarín Solano"
__author_email__ = "jose@bogarin.co.cr"
__contributors__ = [
    "Brad Bester <brbester@cisco.com>",
    "Chris Lunsford <chrlunsf@cisco.com>",
]
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


from webexteamssdk import Webhook
from webexteamssdk.api import WebexTeamsAPI
from cornice import Service
import requests


import logging
log = logging.getLogger(__name__)


# Module constants
CAT_FACTS_URL = 'https://catfact.ninja/fact'


# Initialize the environment
# Create the Webex Teams API connection object
api = WebexTeamsAPI()


# Helper functions
def get_catfact():
    """Get a cat fact from catfact.ninja and return it as a string.

    Functions for Soundhound, Google, IBM Watson, or other APIs can be added
    to create the desired functionality into this bot.

    """
    response = requests.get(CAT_FACTS_URL, verify=False)
    response.raise_for_status()
    json_data = response.json()
    return json_data['fact']


events_service = Service(
    name='events',
    path='/events',
    description="Webex Teams Webhook",
)


@events_service.get()
def get_events_service(request):
    log.info(get_catfact())
    return {"fact": get_catfact()}


# Your Webex Teams webhook should point to http://<serverip>:6543/events
@events_service.post()
def post_events_service(request):
    """Respond to inbound webhook JSON HTTP POST from Webex Teams."""

    # Get the POST data sent from Webex Teams
    json_data = request.json
    log.info("\n")
    log.info("WEBHOOK POST RECEIVED:")
    log.info(json_data)
    log.info("\n")

    # Create a Webhook object from the JSON data
    webhook_obj = Webhook(json_data)

    # Get the room details
    room = api.rooms.get(webhook_obj.data.roomId)

    # Get the message details
    message = api.messages.get(webhook_obj.data.id)

    # Get the sender's details
    person = api.people.get(message.personId)

    log.info("NEW MESSAGE IN ROOM '{}'".format(room.title))
    log.info("FROM '{}'".format(person.displayName))
    log.info("MESSAGE '{}'\n".format(message.text))

    # This is a VERY IMPORTANT loop prevention control step.
    # If you respond to all messages...  You will respond to the messages
    # that the bot posts and thereby create a loop condition.
    me = api.people.me()
    if message.personId == me.id:
        # Message was sent by me (bot); do not respond.
        return {'Message': 'OK'}

    else:
        # Message was sent by someone else; parse message and respond.
        if "/CAT" in message.text:
            log.info("FOUND '/CAT'")

            # Get a cat fact
            catfact = get_catfact()
            log.info("SENDING CAT FACT'{}'".format(catfact))

            # Post the fact to the room where the request was received
            api.messages.create(room.id, text=catfact)
        return {'Message': 'OK'}
