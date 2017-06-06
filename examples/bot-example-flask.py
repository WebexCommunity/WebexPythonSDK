#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""A simple bot script, built on Flask.

This sample script leverages the Flask web service micro-framework
(see http://flask.pocoo.org/).  By default the web server will be reachable at
port 5000 you can change this default if desired (see `flask_app.run(...)`).

ngrok (https://ngrok.com/) can be used to tunnel traffic back to your server
if your machine sits behind a firewall.

You must create a Spark webhook that points to the URL where this script is
hosted.  You can do this via the CiscoSparkAPI.webhooks.create() method.

Additional Spark webhook details can be found here:
https://developer.ciscospark.com/webhooks-explained.html

A bot must be created and pointed to this server in the My Apps section of
https://developer.ciscospark.com.  The bot's Access Token should be added as a
'SPARK_ACCESS_TOKEN' environment variable on the web server hosting this
script.

This script supports Python versions 2 and 3.

"""


from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import json

import requests

from flask import Flask, request

from ciscosparkapi import CiscoSparkAPI, Webhook


# Module constants
CAT_FACTS_URL = 'http://catfacts-api.appspot.com/api/facts?number=1'


# Initialize the environment
flask_app = Flask(__name__)             # Create the web application instance
spark_api = CiscoSparkAPI()             # Create the Cisco Spark API connection object


urls = ('/sparkwebhook', 'webhook')


# Helper functions
def get_catfact():
    """Get a cat fact from appspot.com and return it as a string.

    Functions for Soundhound, Google, IBM Watson, or other APIs can be added
    to create the desired functionality into this bot.

    """
    response = requests.get(CAT_FACTS_URL, verify=False)
    response_dict = json.loads(response.text)
    return response_dict['facts'][0]


# Core bot functionality
@flask_app.route('/sparkwebhook', methods=['GET', 'POST'])                     # Your Spark webhook should point to http://<serverip>:5000/sparkwebhook
def sparkwebhook():
    """Processes incoming requests to the '/sparkwebhook' URI."""
    if request.method == 'GET':
        return (""" <!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <title>Spark Bot served via Flask</title>
                        </head>
                    <body>
                    <p>
                    <strong>Your Flask web server is up and running!</strong>
                    </p>
                    <p>
                    Here is a nice Cat Fact for you:
                    </p>
                    <blockquote> {} </blockquote>
                    </body>
                    </html>
                """.format(get_catfact()))
    elif request.method == 'POST':
        """Respond to inbound webhook JSON HTTP POST from Cisco Spark."""

        json_data = request.json                                               # Get the POST data sent from Cisco Spark
        print("\n")
        print("WEBHOOK POST RECEIVED:")
        print(json_data)
        print("\n")

        webhook_obj = Webhook(json_data)                                       # Create a Webhook object from the JSON data
        room = spark_api.rooms.get(webhook_obj.data.roomId)                    # Get the room details
        message = spark_api.messages.get(webhook_obj.data.id)                  # Get the message details
        person = spark_api.people.get(message.personId)                        # Get the sender's details

        print("NEW MESSAGE IN ROOM '{}'".format(room.title))
        print("FROM '{}'".format(person.displayName))
        print("MESSAGE '{}'\n".format(message.text))

        # This is a VERY IMPORTANT loop prevention control step.
        # If you respond to all messages...  You will respond to the messages
        # that the bot posts and thereby create a loop condition.
        me = spark_api.people.me()
        if message.personId == me.id:
            # Message was sent by me (bot); do not respond.
            return 'OK'

        else:
            # Message was sent by someone else; parse message and respond.
            if "/CAT" in message.text:
                print("FOUND '/CAT'")
                cat_fact = get_catfact()                                       # Get a cat fact
                print("SENDING CAT FACT '{}'".format(cat_fact))
                spark_api.messages.create(room.id, text=cat_fact)              # Post the fact to the room where the request was received
            return 'OK'


if __name__ == '__main__':
    # Start the Flask web server
    flask_app.run(host='0.0.0.0', port=5000)
