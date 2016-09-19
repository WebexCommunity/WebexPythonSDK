#!/usr/bin/python

from ciscosparkapi import CiscoSparkAPI

# VERY simple script to create a room, post a message, and post a file.  Alternaitvely, if the room already exists it will delete the room.


#storing the Authentication token in a file in the OS vs. leaving in script
# see https://developer.ciscospark.com/getting-started.html to copy your token and simply place in a text file
fat=open ("/home/brad/brad_at.txt","r+")  #open the file with the token
access_token=fat.readline().rstrip()      #strip whitespace, newline, etc.
fat.close                                 #close file

room_name="TEST Hello World Room"         #set the name of our test room - PLEASE NOTE this room can be delted by script so don't use a current name
room_count=0
test_message="Hello World"                #set the test message we will post
test_url=["https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Cisco_logo.svg/375px-Cisco_logo.svg.png"] #set the location of  a file we will post

api = CiscoSparkAPI(access_token)         #invoke the API

rooms = api.rooms.list()                  #grab the list of rooms where the user(from Access Token) is a member


for room in rooms:                        #iterate through list of rooms
    if room.title == room_name:           #look for our room
         room_count += 1                  #if we find a room with the same name increment a counter
         print (room.title)  
         room_id = room.id                #grab the room id
         print (room_id)
         api.rooms.delete(room_id)        #delete the room
         print ("Room Deleted")

if (room_count == 0):                     #Otherwise create the room, post a message, add a user,  and attachment                   
    room = api.rooms.create(room_name)    #create a room with room_name  - room.id will be the id of this new room
    print room                            #prints returned JSON                      
    message = api.messages.create(room.id,None,None,test_message)       #create a message in the new room
    print message 
    message = api.messages.create(room.id,None,None,None,None,test_url) #Post a file in the new room from test_url
    print message





