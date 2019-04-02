import os
import sys
from webexteamssdk import WebexTeamsAPI, ApiError

cwd  = os.path.abspath(os.path.dirname('.'))
sys.path.append(cwd)
testfile = '/'+cwd+'/test.png' #expected format: '//Users/userid/dir/test.png'

file_list = []
file_list.append(testfile)

token = 'your_bot_token'
api = WebexTeamsAPI(access_token=token)
headers = {'Authorization': 'Bearer '+token}

api.messages.create(roomId='your_room_id', files=file_list)
