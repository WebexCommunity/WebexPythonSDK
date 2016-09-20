#!/usr/bin/python

# This is a simple bot script.  You must create a Spark webhook that points to the server where this script runs
# ngrok can be used to tunnel traffic back to this server if you don't wish to expose your test machine publicly to the Internet
# By default this server will be reachable at port 8080 - append a different port when launching the script if desired
# Additional Spark webhook details can be found here - https://developer.ciscospark.com/webhooks-explained.html
#
# A bot must be created and pointed to this server in the My Apps section of https://developer.ciscospark.com
# The bot's Access Token should be placed in a directory on the system running this script and the file_name should be updated below
#
# Sample Webhook:
# {
#	"id": "Y2lzY29..........mE4U1XXW3323",
#	"name": "Example Webhook",
#	"targetUrl": "http://<yourserverurl>.com:56811/sparkwebhook",
#	"resource": "messages",
#	"event": "created",
#	"secret": "supersecret",
#	"created": "2016-09-20T18:29:06.920Z"
# }
#

import web
import json
import requests
from ciscosparkapi import CiscoSparkAPI

#
# CHANGE this to your bot Access Token file
#
file_name="/home/brad/ciscosparkapiexamples/botat.txt"

#this function gets a cat fact from appspot.com and returns it as a string
#functions for Soundhound, Google, IBM Watson, or other APIs can be added to build desired functionality into this bot
def get_catfact():
    URL = 'http://catfacts-api.appspot.com/api/facts?number=1'
    resp = requests.get(URL, verify=False)
    resp_dict = json.loads(resp.text)
    return resp_dict["facts"][0]


fat=open (file_name,"r+")  #open the file with the token 

access_token=fat.readline().rstrip()      #strip whitespace, newline, etc. 

fat.close



urls = ('/sparkwebhook', 'webhook')       #webhook should point to http://<serverip>:8080/sparkwebhook

app = web.application(urls, globals())    #create a web application instance

api = CiscoSparkAPI(access_token)         #invoke the API

# This section defines what to do when a webhook is received from Spark
class webhook:
    def POST(self):                                                       #webhook are received via HTTP POST
        data = web.data()                                                 #grabs the data sent from Spark
    
        print
        print 'DATA RECEIVED:'
        print data
        print
    
        json_data = json.loads(data)                                      #loads the data as JSON format
        room_id = json_data["data"]["roomId"]                             #grabs the roomId
        message_id = json_data["data"]["id"]                              #grabs the messageId
    
        print room_id
        print message_id
       
        message=api.messages.get(message_id)                              #grabs the actual message detail
    
        print message      
    
        message_text = message.text                                       #grabs the message text
    
        print message_text

#THIS IS VERY IMPORTANT LOOP CONTROL
#if you respond to all messages you will respond to the bot and create a loop condition
#Alternatively you could look at the posting room member and filter your bot's messages

        if ((message_text.find("\CAT", 10, 20)) > -1):                    #looks for \CAT between position 10 and 20 in message string
    
            print "Found \CAT"
    
            cat_fact=get_catfact()                                        #grabs a cat fact
            message_post = api.messages.create(room_id,None,None,cat_fact)#posts the fact in the room where request received
    
            print message_post
    
        return 'OK'


     
if __name__ == '__main__':
    app.run()                                                             #starts listening for incoming webhooks



