#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""Sample script to read local ngrok info and create a corresponding webhook.

Sample script that reads ngrok info from the local ngrok client api and creates
a Cisco Spark Webhook pointint to the ngrok tunnel's public HTTP URL.

Typically ngrok is called run with the following syntax to redirect an
Internet accesible ngrok url to localhost port 8080:

    $ ngrok http 8080

To use script simply launch ngrok, and then launch this script.  After ngrok is
killed, run this script a second time to remove webhook from Cisco Spark.

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


import sys

from ciscosparkapi import CiscoSparkAPI
import requests


# Find and import urljoin
if sys.version_info[0] < 3:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin


# Constants
NGROK_CLIENT_API_BASE_URL = "http://localhost:4040/api"
WEBHOOK_NAME = "ngrok_webhook"
WEBHOOK_URL_SUFFIX = "/sparkwebhook"
WEBHOOK_RESOURCE = "messages"
WEBHOOK_EVENT = "created"


def get_ngrok_public_url():
    """Get the ngrok public HTTP URL from the local client API."""
    try:
        response = requests.get(url=NGROK_CLIENT_API_BASE_URL + "/tunnels",
                                headers={'content-type': 'application/json'})
        response.raise_for_status()

    except requests.exceptions.RequestException:
        print("Could not connect to the ngrok client API; "
              "assuming not running.")
        return None

    else:
        for tunnel in response.json()["tunnels"]:
            if tunnel.get("public_url", "").startswith("http://"):
                print("Found ngrok public HTTP URL:", tunnel["public_url"])
                return tunnel["public_url"]


def delete_webhooks_with_name(spark_api, name):
    """Find a webhook by name."""
    for webhook in spark_api.webhooks.list():
        if webhook.name == name:
            print("Deleting Webhook:", webhook.name, webhook.targetUrl)
            spark_api.webhooks.delete(webhook.id)


def create_ngrok_webhook(spark_api, ngrok_public_url):
    """Create a Cisco Spark webhook pointing to the public ngrok URL."""
    print("Creating Webhook...")
    webhook = spark_api.webhooks.create(
        name=WEBHOOK_NAME,
        targetUrl=urljoin(ngrok_public_url, WEBHOOK_URL_SUFFIX),
        resource=WEBHOOK_RESOURCE,
        event=WEBHOOK_EVENT,
    )
    print(webhook)
    print("Webhook successfully created.")
    return webhook


def main():
    """Delete previous webhooks. If local ngrok tunnel, create a webhook."""
    spark_api = CiscoSparkAPI()
    delete_webhooks_with_name(spark_api, name=WEBHOOK_NAME)
    public_url = get_ngrok_public_url()
    if public_url is not None:
        create_ngrok_webhook(spark_api, public_url)


if __name__ == '__main__':
    main()
