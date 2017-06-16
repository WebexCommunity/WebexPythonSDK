"""A simple bot script, built on Pyramid using Cornice

This sample script leverages the Pyramid web framework (https://trypyramid.com/) with
Cornice (https://cornice.readthedocs.io).  By default the web server will be reachable at
port 6543 you can change this default if desired (see `pyramidSparkBot.ini`).

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
from cornice import Service

from builtins import *

import json

import requests

from ciscosparkapi import CiscoSparkAPI, Webhook

import logging
log = logging.getLogger(__name__)


# Module constants
CAT_FACT_URL = 'http://catfacts-api.appspot.com/api/facts?number=1'


# Initialize the environment
spark_api = CiscoSparkAPI()             # Create the Cisco Spark API connection object


# Helper functions
def get_catfact():
    """Get a cat fact from catfacts-api.appspot.com and return it as a string.
    Functions for Soundhound, Google, IBM Watson, or other APIs can be added
    to create the desired functionality into this bot.
    """
    response = requests.get(CAT_FACT_URL, verify=False)
    response_dict = json.loads(response.text)
    return response_dict['facts'][0]


sparkwebhook = Service(name='sparkwebhook', path='/sparkwebhook', description="Spark Webhook")


@sparkwebhook.get()
def get_sparkwebhook(request):
    log.info(get_catfact())
    return {"fact": get_catfact()}

@sparkwebhook.post()
# Your Spark webhook should point to http://<serverip>:6543/sparkwebhook
def post_sparkwebhook(request):
    """Respond to inbound webhook JSON HTTP POST from Cisco Spark."""

    json_data = request.json                                               # Get the POST data sent from Cisco Spark
    log.info("\n")
    log.info("WEBHOOK POST RECEIVED:")
    log.info(json_data)
    log.info("\n")

    webhook_obj = Webhook(json_data)                                       # Create a Webhook object from the JSON data
    room = spark_api.rooms.get(webhook_obj.data.roomId)                    # Get the room details
    message = spark_api.messages.get(webhook_obj.data.id)                  # Get the message details
    person = spark_api.people.get(message.personId)                        # Get the sender's details

    log.info("NEW MESSAGE IN ROOM '{}'".format(room.title))
    log.info("FROM '{}'".format(person.displayName))
    log.info("MESSAGE '{}'\n".format(message.text))

    # This is a VERY IMPORTANT loop prevention control step.
    # If you respond to all messages...  You will respond to the messages
    # that the bot posts and thereby create a loop condition.
    me = spark_api.people.me()
    if message.personId == me.id:
        # Message was sent by me (bot); do not respond.
        return {'Message': 'OK'}

    else:
        # Message was sent by someone else; parse message and respond.
        if "/CAT" in message.text:
            log.info("FOUND '/CAT'")
            catfact = get_catfact()                                       # Get a cat fact
            log.info("SENDING CAT FACT'{}'".format(catfact))
            spark_api.messages.create(room.id, text=catfact)              # Post the fact to the room where the request was received
        return {'Message': 'OK'}

