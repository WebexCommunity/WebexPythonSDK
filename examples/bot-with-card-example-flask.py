#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""A simple bot script, built on Flask, that demonstrates posting a
card, and handling the events generated when a user hits the Submit button.

A bot must be created and pointed to this server in the My Apps section of
https://developer.webex.com.  The bot's Access Token should be added as a
'WEBEX_TEAMS_ACCESS_TOKEN' environment variable on the web server hosting this
script.

This script must expose a public IP address in order to receive notifications
about Webex events.  ngrok (https://ngrok.com/) can be used to tunnel traffic
back to your server if your machine sits behind a firewall.

The following environment variables are needed for this to run

* WEBEX_TEAMS_ACCESS_TOKEN -- Access token for a Webex bot
* WEBHOOK_URL -- URL for Webex Webhooks (ie: https://2fXX9c.ngrok.io)
* PORT - Port for Webhook URL (ie: the port param passed to ngrok)

This sample script leverages the Flask web service micro-framework
(see http://flask.pocoo.org/).  By default the web server will be reachable at
port 5000 you can change this default if desired (see `flask_app.run(...)`).
In our app we read the port from the PORT environment variable.

Upon startup this app create webhooks so that our bot is notified when users
send it messages or interact with any cards that have been posted.   In
response to any messages it will post a simple form filling card.  In response
to a user submitting a form, the details of that response will be posted in
the space.

This script should supports Python versions 2 and 3, but it has only been
tested with version 3.

Copyright (c) 2016-2020 Cisco and/or its affiliates.

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


__author__ = "JP Shipherd"
__author_email__ = "jshipher@cisco.com"
__contributors__ = ["Chris Lunsford <chrlunsf@cisco.com>"]
__copyright__ = "Copyright (c) 2016-2020 Cisco and/or its affiliates."
__license__ = "MIT"

from flask import Flask, request
from signal import signal, SIGINT
import requests
import sys

from webexteamssdk import WebexTeamsAPI, Webhook

# Find and import urljoin
if sys.version_info[0] < 3:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin

# Constants
WEBHOOK_NAME = "botWithCardExampleWebhook"
WEBHOOK_URL_SUFFIX = "/events"
MESSAGE_WEBHOOK_RESOURCE = "messages"
MESSAGE_WEBHOOK_EVENT = "created"
CARDS_WEBHOOK_RESOURCE = "attachmentActions"
CARDS_WEBHOOK_EVENT = "created"

# Adaptive Card Design Schema for a sample form.
# To learn more about designing and working with buttons and cards,
# checkout https://developer.webex.com/docs/api/guides/cards
card_content = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.0",
    "body": [
        {
            "type": "TextBlock",
            "text": "Some ways to collect user input",
            "size": "medium",
            "weight": "bolder"
        },
        {
            "type": "TextBlock",
            "text": "This **Input.Text** element collects some free from text.  \
              Designers can use attributes like `isMutiline`, `maxLength` and `placeholder` \
                to shape the way that users enter text in a form.",
            "wrap": True
        },
        {
            "type": "Input.Text",
            "placeholder": "Text Field",
            "style": "text",
            "maxLength": 0,
            "id": "TextFieldVal"
        },
        {
            "type": "TextBlock",
            "text": "This **Input.Number** element collects a number.  \
              Designers can use the `max`, `min` and `placeholder` attributes \
                to control the input options.",
            "wrap": True
        },
        {
            "type": "Input.Number",
            "placeholder": "Number",
            "min": -5,
            "max": 5,
            "id": "NumberVal"
        },
        {
            "type": "TextBlock",
            "text": "The **Input.ChoiceSet** element provides a variety of ways that users \
              can choose from a set of options.   This is the default view, but designers can \
                use the `style` and `isMutiSelect` attributes to change the way it works.  \
                  The choices are defined in an array attribute called `choices`.",
            "wrap": True
        },
        {
            "type": "Input.ChoiceSet",
            "id": "ColorChoiceVal",
            "value": "Red",
            "choices": [
                {
                    "title": "Red",
                    "value": "Red"
                },
                {
                    "title": "Blue",
                    "value": "Blue"
                },
                {
                    "title": "Green",
                    "value": "Green"
                }
            ]
        },
        {
            "type": "Input.Toggle",
            "title": "This Input.Toggle element gets a true/false input.",
            "id": "Toggle",
            "wrap": True,
            "value": "false"
        }
    ],
    "actions": [
        {
            "type": "Action.Submit",
            "title": "Submit",
            "data": {
                "formDemoAction": "Submit"
            }
        }
    ]
}

# Read required environment variables
import os
port = 0
webhook_url = ""
try:
    webhook_url = os.environ['WEBHOOK_URL']
    port = int(os.environ['PORT'])
    os.environ['WEBEX_TEAMS_ACCESS_TOKEN']
except KeyError:
    print('''
    Missing required environment variable.  You must set:
    * WEBEX_TEAMS_ACCESS_TOKEN -- Access token for a Webex bot\n
    * WEBHOOK_URL -- URL for Webex Webhooks (ie: https://2fXX9c.ngrok.io)
    * PORT - Port for Webhook URL (ie: the port param passed to ngrok)
    '''
         )
    sys.exit

# Initialize the environment
# Create the web application instance
flask_app = Flask(__name__)
# Create the Webex Teams API connection object
api = WebexTeamsAPI()


# Helper functions
def delete_webhooks_with_name(api):
    """List all webhooks and delete ours."""
    for webhook in api.webhooks.list():
        if webhook.name == WEBHOOK_NAME:
            print("Deleting Webhook:", webhook.name, webhook.targetUrl)
            api.webhooks.delete(webhook.id)

def create_webhooks(api, webhook_url):
    """Create the Webex Teams webhooks we need for our bot."""
    print("Creating Message Created Webhook...")
    webhook = api.webhooks.create(
        resource=MESSAGE_WEBHOOK_RESOURCE,
        event=MESSAGE_WEBHOOK_EVENT,
        name=WEBHOOK_NAME,
        targetUrl=urljoin(webhook_url, WEBHOOK_URL_SUFFIX)
    )
    print(webhook)
    print("Webhook successfully created.")

    print("Creating Attachment Actions Webhook...")
    webhook = api.webhooks.create(
        resource=CARDS_WEBHOOK_RESOURCE,
        event=CARDS_WEBHOOK_EVENT,
        name=WEBHOOK_NAME,
        targetUrl=urljoin(webhook_url, WEBHOOK_URL_SUFFIX)
    )
    print(webhook)
    print("Webhook successfully created.")

def respond_to_button_press(api, webhook):
    """Respond to a button press on the card we posted"""

    # Some server side debugging
    room = api.rooms.get(webhook.data.roomId)
    attachment_action = api.attachment_actions.get(webhook.data.id)
    person = api.people.get(attachment_action.personId)
    message_id = attachment_action.messageId
    print("NEW BUTTON PRESS IN ROOM '{}'".format(room.title))
    print("FROM '{}'".format(person.displayName))

    api.messages.create(
        room.id,
        parentId=message_id,
        markdown=f'This is the data sent from the button press.  A more robust app would do something cool with this:\n```\n{attachment_action.to_json(indent=2)}\n```'
    )

def respond_to_message(api, webhook):
    """Respond to a message to our bot"""

    # Some server side debugging
    room = api.rooms.get(webhook.data.roomId)
    message = api.messages.get(webhook.data.id)
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
        api.messages.create(room.id, text="All I do is post a sample card.  Here it is:")
        api.messages.create(
            room.id,
            text="If you see this your client cannot render cards",
            attachments=[{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card_content
            }]
        )
        return 'OK'

# Signal handler to clean up webhooks when we shutdown
def signal_handler(sig, frame):
    """Cleanup webhooks on shutdown"""
    print('You pressed Ctrl+C! Cleaning up webhooks...')
    delete_webhooks_with_name(api)
    sys.exit(0)

# Core bot functionality
# Webex will post to this server when a message is created for the bot
# or when a user clicks on an Action.Submit button in a card posted by this bot
# Your Webex Teams webhook should point to http://<serverip>:<port>/events
@flask_app.route('/events', methods=["POST"])
def webex_teams_webhook_events():
    """Respond to inbound webhook JSON HTTP POST from Webex Teams."""
    # Create a Webhook object from the JSON data
    webhook_obj = Webhook(request.json)

    # Handle a new message event
    if webhook_obj.resource == MESSAGE_WEBHOOK_RESOURCE and \
        webhook_obj.event == MESSAGE_WEBHOOK_EVENT:
        respond_to_message(api, webhook_obj)

    # Handle an Action.Submit button press event
    elif webhook_obj.resource == CARDS_WEBHOOK_RESOURCE and \
        webhook_obj.event == CARDS_WEBHOOK_EVENT:
        respond_to_button_press(api, webhook_obj)

    # Ignore anything else (which should never happen
    else:
        print("IGNORING UNEXPECTED WEBHOOK:")
        print(webhook_obj)

    return 'OK'


def main():
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, signal_handler)
    delete_webhooks_with_name(api)
    create_webhooks(api, webhook_url)
    # Start the Flask web server
    flask_app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
