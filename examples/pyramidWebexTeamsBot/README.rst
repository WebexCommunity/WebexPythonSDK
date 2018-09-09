Documentation
=============

A simple bot script, built on Pyramid using Cornice.

This sample script leverages the Pyramid web framework https://trypyramid.com/
with Cornice https://cornice.readthedocs.io.  By default the web server will be
reachable at port 6543 you can change this default if desired
(see `pyramidWebexTeamsBot.ini`).

ngrok (https://ngrok.com/) can be used to tunnel traffic back to your server
if your machine sits behind a firewall.

You must create a Webex Teams webhook that points to the URL where this script is
hosted.  You can do this via the WebexTeamsAPI.webhooks.create() method.

Additional Webex Teams webhook details can be found here:
https://developer.webex.com/webhooks-explained.html

A bot must be created and pointed to this server in the My Apps section of
https://developer.webex.com.  The bot's Access Token should be added as a
'WEBEX_TEAMS_ACCESS_TOKEN' environment variable on the web server hosting this
script.

This script supports Python versions 2 and 3.

Running the bot
-------------------

In order to execute the bot, you need to

``python setup.py develop``
``pserve --reload pyramidWebexTeamsBot``
