#sample script that reads ngrok info from localhost:4040 and create Cisco Spark Webhook
#typicall ngrok is called "ngrok http 8080" to redirect localhost:8080 to Internet
#accesible ngrok url
#
#To use script simply launch ngrok, then launch this script.  After ngrok is killed, run this
#script a second time to remove webhook from Cisco Spark


import requests
import json
import re
import sys
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
from ciscosparkapi import CiscoSparkAPI, Webhook

def findwebhookidbyname(api, webhookname):
    webhooks = api.webhooks.list()
    for wh in webhooks:
        if wh.name == webhookname:
            return wh.id
    return "not found"

#Webhook attributes
webhookname="testwebhook"
resource="messages"
event="created"
url_suffix="/sparkwebhook"

#grab the at from a local at.txt file instead of global variable
fat=open ("at.txt","r+")
at=fat.readline().rstrip()
fat.close

api = CiscoSparkAPI(at)

#go to the localhost page for nogrok and grab the public url for http
try:
    ngrokpage = requests.get("http://127.0.0.1:4040").text
except:
    print ("no ngrok running - deleting webhook if it exists")
    whid=findwebhookidbyname(api, webhookname)
    if "not found" in whid:
        print ("no webhook found")
        sys.exit()
    else:
        print (whid)
        dict=api.webhooks.delete(whid)
        print (dict)
        print ("Webhook deleted")
        sys.exit()

for line in ngrokpage.split("\n"):
    if "window.common = " in line:
        ngrokjson = re.search('JSON.parse\(\"(.+)\"\)\;',line).group(1)
        ngrokjson = (ngrokjson.replace('\\',''))
print (ngrokjson)
Url = (json.loads(ngrokjson)["Session"]["Tunnels"]["command_line (http)"]["URL"])+url_suffix
print (Url)

#check if the webhook exists by name and then create it if not
whid=findwebhookidbyname(api, webhookname)

if "not found" in whid:
    #create
    print ("not found")
    dict=api.webhooks.create(webhookname, Url, resource, event)
    print (dict)
else:
    #update
    print (whid)
    dict=api.webhooks.update(whid, name=webhookname, targetUrl=Url) 
    print (dict)
