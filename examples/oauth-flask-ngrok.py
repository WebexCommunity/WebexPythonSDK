#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""Implementation of OAuth for Webex Integration with Flask and ngrok.

This sample script leverages the Flask web service micro-framework (see
https://flask.palletsprojects.com/).

Ngrok (https://ngrok.com/) can be used to tunnel traffic back to your server if
your machine sits behind a firewall. Free account registration required. Ngrok
is launched with "./ngrok http 5000"

You must create a Webex Integration in the My Webex Apps section of
https://developer.webex.com. For details, see
https://developer.webex.com/docs/integrations .
Copy your integration Client ID, Client Secret, scopes and set Redirect URI as
"http://localhost:5000/callback" or the public ngrok URI + "/callback".

Copyright (c) 2022 Cisco and/or its affiliates.

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


from flask import Flask, url_for, session, redirect, request
import urllib.parse
from uuid import uuid4
import requests

from webexteamssdk import WebexTeamsAPI

# Parameters configured in Webex Integration
OAUTH_CLIENT_ID = "your integration Client ID"
OAUTH_CLIENT_SECRET = "your integration Client Secret"
OAUTH_CALLBACK_URI = "http://localhost:5000/callback"
# Scopes are space-separated. Can use any subset of the configured scopes.
OAUTH_SCOPE = "spark:people_read meeting:schedules_read"

# Static Webex URIs
oauth_authorizationUri = "https://webexapis.com/v1/authorize?"
oauth_tokenUri = "https://webexapis.com/v1/access_token"

# On a local machine, this script will run even without a public callback URI.
# But in reality the user is never on the same computer with the server. To
# enable remote user access, an Ngrok public URI has to be used instead of the
# local URI.
# Uncomment the lines below to automatically get the public URI from
# ngrok and use it instead of the local one. This public URI must also be
# configured in the Webex Integration as a Redirect URI.
#
# r = requests.get("http://localhost:4040/api/tunnels")
# public_url = r.json()['tunnels'][0]['public_url']
# OAUTH_CALLBACK_URI = public_url + "/callback"

# Create Flask app instance
app = Flask(__name__)

# Flask secret key is required to use session
app.secret_key = "very bad secret"


# Welcome page. Link to auth from this page, or from anywhere else.
@app.route("/")
def root():
    print("/ requested")
    return """
            <p>Hey, this is Flask!</p>
            <p>Click <a href="{}">here</a> to authorize Webex Integration.</p>
            """.format(url_for("auth"))


# OAuth Step 1 - Build authorization URL and redirect user.
# Redirect the user/resource owner to the OAuth provider (Webex) using an URI
# with a few key OAuth parameters.
@app.route("/auth")
def auth():
    print("Authorization requested")

    # State is used to prevent CSRF, generate random and save in session.
    # Not mandatory but improves security.
    oauth_state = str(uuid4())
    session["oauth_state"] = oauth_state

    # All parameters we need to pass to authorization service
    oauth_params = {
        "response_type": "code",
        "client_id": OAUTH_CLIENT_ID,
        "redirect_uri": OAUTH_CALLBACK_URI,
        "scope": OAUTH_SCOPE,
        "state": oauth_state,
    }
    authorizationUri = oauth_authorizationUri + urllib.parse.urlencode(
        oauth_params
    )

    return redirect(authorizationUri)


# OAuth Step 2 - User authorization.
# This happens on the provider side.


# OAuth Step 3 - Receive authorization code and obtain access token.
# The user has been redirected back from the provider to your registered
# callback URI. With this request comes an authorization code included in the
# redirect URI. We will use that code to obtain an access token. The access
# token can be then used for any API calls within the authorized scopes.
@app.route("/callback", methods=["GET"])
def callback():
    print("OAuth callback received")

    oauth_error = request.args.get("error_description", "")
    if oauth_error:
        return "OAuth error: " + oauth_error

    oauth_code = request.args.get("code")
    if not oauth_code:
        return (
            "OAuth error: Authorization provider did not return authorization "
            "code."
        )

    # check state to prevent CSRF
    oauth_state = request.args.get("state", "")
    if not oauth_state:
        return "OAuth error: Authorization provider did not return state."
    if oauth_state != session["oauth_state"]:
        return "OAuth error: State does not match."

    # There are three options how the OAuth authorization code can be used

    # 1.
    # The API connection can be directly initialized with OAuth information. It
    # will exchange the OAuth authorization code to an access token behind the
    # scenes. It is the easiest, but the drawback is the refresh token is lost
    # and cannot be saved.
    api = WebexTeamsAPI(
        client_id=OAUTH_CLIENT_ID,
        client_secret=OAUTH_CLIENT_SECRET,
        oauth_code=oauth_code,
        redirect_uri=OAUTH_CALLBACK_URI,
    )
    print(api.people.me())
    return "Welcome, {}!".format(api.people.me().displayName)

    # 2.
    # The API connection object can be initialized with any string. Then use
    # the access_tokens endpoint to obtain access and refresh tokens. The
    # access token is valid for 14 days. The refresh token may be saved
    # somewhere and later used to refresh the access token with
    # access_tokens.refresh()
    # api = WebexTeamsAPI("any string")
    # access_tokens = api.access_tokens.get(
    #     client_id=OAUTH_CLIENT_ID,
    #     client_secret=OAUTH_CLIENT_SECRET,
    #     code=oauth_code,
    #     redirect_uri=OAUTH_CALLBACK_URI
    # )
    # access_token = access_tokens.access_token
    # refresh_token = access_tokens.refresh_token
    # # Reinit API connection with the obtained access_token
    # api.__init__(access_token)
    # print(api.people.me())
    # return "Welcome, {}!".format(api.people.me().displayName)

    # 3.
    # Alternatively, can use requests to exchange authorization code to access
    # token without using the Webex SDK. Useful if your authorization process
    # is separate from the token usage. Save tokens somewhere for later use.
    # oauth_data = {
    #     'grant_type': "authorization_code",
    #     'redirect_uri': OAUTH_CALLBACK_URI,
    #     'code': oauth_code,
    #     'client_id': OAUTH_CLIENT_ID,
    #     'client_secret': OAUTH_CLIENT_SECRET
    # }
    # resp = requests.post(oauth_tokenUri, data=oauth_data)
    # if not resp.ok:
    #     return (
    #         "OAuth error: Authorization provider returned:<br>{}"
    #         "".format(resp.json()['error_description'])
    #     )
    # else:
    #     oauth_tokens = resp.json()
    #     access_token = oauth_tokens["access_token"]
    #     refresh_token = oauth_tokens["refresh_token"]
    #     # save tokens
    # return "Authorization successful."


if __name__ == "__main__":
    # Start Flask web server
    app.run(port=5000)
