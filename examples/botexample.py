#!/usr/bin/env python2
#  -*- coding: utf-8 -*-
"""A simple bot script.

This sample script leverages web.py (see http://webpy.org/).  By default the
web server will be reachable at port 8080 - append a different port when
launching the script if desired.  ngrok can be used to tunnel traffic back to
your server if you don't wish to expose your machine publicly to the Internet.

You must create a Spark webhook that points to the URL where this script is
hosted.  You can do this via the CiscoSparkAPI.webhooks.create() method.

Additional Spark webhook details can be found here:
https://developer.ciscospark.com/webhooks-explained.html

A bot must be created and pointed to this server in the My Apps section of
https://developer.ciscospark.com.  The bot's Access Token should be added as a
'SPARK_ACCESS_TOKEN' environment variable on the web server hosting this
script.

NOTE:  While this script is written to support Python versions 2 and 3, as of
the time of this writing web.py (v0.38) only supports Python 2.
Therefore this script only supports Python 2.

"""


from __future__ import print_function
from builtins import object

import json

import web
import requests

from ciscosparkapi import CiscoSparkAPI, Webhook


# Module constants
CAT_FACTS_URL = 'http://catfacts-api.appspot.com/api/facts?number=1'


# Global variables
urls = ('/sparkwebhook', 'webhook')       # Your Spark webhook should point to http://<serverip>:8080/sparkwebhook
app = web.application(urls, globals())    # Create the web application instance
api = CiscoSparkAPI()                     # Create the Cisco Spark API connection object


def get_catfact():
    """Get a cat fact from appspot.com and return it as a string.

    Functions for Soundhound, Google, IBM Watson, or other APIs can be added
    to create the desired functionality into this bot.

    """
    response = requests.get(CAT_FACTS_URL, verify=False)
    response_dict = json.loads(response.text)
    return response_dict['facts'][0]


class webhook(object):
    def POST(self):
        """Respond to inbound webhook JSON HTTP POSTs from Cisco Spark."""
        json_data = web.data()                                  # Get the POST data sent from Spark
        print("\nWEBHOOK POST RECEIVED:")
        print(json_data, "\n")

        webhook_obj = Webhook(json_data)                        # Create a Webhook object from the JSON data
        room = api.rooms.get(webhook_obj.data.roomId)           # Get the room details
        message = api.messages.get(webhook_obj.data.id)         # Get the message details
        person = api.people.get(message.personId)               # Get the sender's details

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
                cat_fact = get_catfact()                                          # Get a cat fact
                print("SENDING CAT FACT '{}'".format(cat_fact))
                response_message = api.messages.create(room.id, text=cat_fact)    # Post the fact to the room where the request was received
        return 'OK'


if __name__ == '__main__':
    # Start the web.py web server
    app.run()
