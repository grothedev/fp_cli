#this is the official python CLI program for Frog Pond
#TODO copyright header


import os
import sys
from pathlib import Path
import getopt
import requests
import json
import datetime
import re
from enum import Enum
#########################



#########################
# FUNCTIONS #
###

#shows a croak in a pretty way
def displayCroak(c):
    formatData(c)
    print('Croak ' + str(c['id']) + ': ' + c['created_at']);
    print('  ' + c['content']);
    print('  Tags: ' + c['tags_str']);
    print();
    
def displayCroakDetail(c):
    displayCroak(c)
    print("  Comments:")
    resp = requests.get(apiurl+'croaks?pid='+c['id'])
    comments = json.loads(resp.text)
    displayCroakList(comments)
    
def displayCroakList(croaks, withComments=False):
    for c in croaks:
        displayCroak(c)
    

#assoc human-readable timestamp, tag list, etc.
def formatData(c):
    ts = '';
    for t in c['tags']:
        ts += t['label'] + ', ';
    ts = ts[:len(ts)-2]; #remove extra comma
    c['tags_str'] = ts;

    #c['timestamp'] = datetime.datetime.strptime(c['created_at'], '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d at %H:%M');

def createCroak():
    content = input('Type your croak.\n');
    filePath = input('If you would like to attach a file, enter the path. Otherwise leave blank.\n');
    sugTags = ''; #TODO
    tags = input('Enter some tags to which this croak is related.\n');
    re.sub(' ', ',', tags) #replace spaces with commas for API compat
    postData = {
        'content': content,
        'tags': tags,
        'x': lon, 'y': lat
    }
    resp = None
    if filePath != None and filePath != '':
        filesData = {'f': ('f', open(filePath, 'rb'))}
        headers = {'content-type': 'multipart/form-data'}
        resp = requests.post(apiurl+'croaks', data=postData, files=filesData, headers=headers)
    else:
        resp = requests.post(apiurl+'croaks', data=postData)
    print(resp.text) #TODO handle response

def displayCroakDetail(croakID):
    resp = requests.get(apiurl+'croaks/'+croakID)
    
def voteOnCroak(croakID, vote):
    resp = requests.post(apiurl+'votes', vote)
    print(resp.text)
    
def back():
    return
    
class STATE(Enum):
    INIT=0
    CROAKFEED=1
    CROAKDETAIL=2
    CROAKCREATE=3
    #CROAKREPLY=4
    
class ACTIONTYPE(Enum):
    CROAKDETAIL=0
    BACK=1
    CROAKCREATE=2
    VOTE=3
    REPLY=4
    
class UserAction:
    action = None
    payload = None
    def __init__(self, action, payload=None):
        self.action = action
        self.payload = payload
##########################

##########################
# GLOBAL VARS #
###
tagsStr=''
tagsExclusive=False
radius=15 # default radius of km
apiurl='http://grothe.ddns.net:8090/api/'
lat=None
lon=None
query=apiurl+"croaks?"
APPDIR=str(Path.home()) + '/.frogpond/'
printRaw=False
state=STATE.INIT
###########################


###
# SETUP #
###
if not os.path.isdir(APPDIR):
    if not os.path.exists(APPDIR):
        os.mkdir(APPDIR);
        print("Made app directory " + APPDIR);
    else:
        print("Error: another file exists at " + APPDIR);

#use location service to get lat lon
locStr = requests.get("http://ipinfo.io/loc").text
locStrArr = locRes.split(',')
lat = lacStrArr[0]
lon = lacStrArr[1]

#get command, make api request, present formatted results

#TODO check last query time? or add option for cached croaks?



###
# INPUT PARSING #
###
opts, extra = getopt.getopt(sys.argv[1:], "hRr:t:l:m:ci:");

for o, a in opts:
    if o == '-h':
        print('TODO display help');
        sys.exit(0)
    elif o == '-c': #create a croak
        createCroak()
        state = STATE.CROAKCREATE
        sys.exit(0) #TODO exit or continue to user interaction?
    elif o == '-R': #raw data: don't format; direct API response
        printRaw = True
    elif o == '-i': #get croak by id
        query = apiurl + 'croaks/' + str(a);
        state = STATE.CROAKDETAIL
    elif o == '-r': # radius
        radius = int(a)
        state = STATE.CROAKFEED
    elif o == '-m': # "mode". exclusive or inclusive tags
        if a != 0:
            tagsExclusive = True
    elif o == '-t': # specify tags
        tagsStr = a
        re.sub(' ', ',', tagsStr)
        tagSet = 'all' if tagsExclusive else 'any'
        print('Gathering croaks which contain ' + tagSet + ' of the following tags: ' + tagsStr.split(','))
        state = STATE.CROAKFEED
    elif o == '-l': # limit number of results
        if a != None:
            query += 'n=' + str(a) + '&';
        state = STATE.CROAKFEED

if tagsStr != '':
    query += 'tags=' + tagsStr + '&';
query += 'x='+lon + 'y='+lat + 'radius='+radius

resp = requests.get(str(query)).text;
croaks = json.loads(resp);


###
# OUTPUT #
###

if printRaw:
    print(res.decode('utf-8'))
else:
    print("~   ~  ~~ ~~~~~ ~~  ~   ~\nWelcome to the Pond!\n")
    displayCroakList(croaks)
    print("~   ~  ~~ ~~~~~ ~~  ~   ~");
    
###
# USER INTERACTION LOOP
###
# wait for input for action
# perform action
# display resulting output
# repeat

userAction = None
while True:
    if state == STATE.CROAKFEED:
        print('Select a croak to view details of by number in the list. Or select another action.')
        print('C: Create Croak')
        print('Q: Quit')
    elif state == STATE.CROAKDETAIL:
        print('Select a comment to view details. Or select another action.')
        print('C: Comment on this Croak')
        print('B: Back')
        print('U: Upvote')
        print('D: Downvote')
        print('Q: Quit')
    else:
        print('what state are you in?')

    while True
        try:
            userActionStr = input()
            if isinstance(userActionStr, int):
                userAction = UserAction(ACTION.CROAKDETAIL, int(userActionStr))
                break;
            else:
                if userActionStr.lower() == 'q':
                    sys.exit(0)
                elif userActionStr.lower() == 'c':
                    userAction = UserAction(ACTION.CROAKCREATE)
                    break;
                else:
                    print('Not a valid action: ' + userActionStr)
        except:
            print('Not a valid action')

    if userAction.action == ACTION.CROAKDETAIL:
        displayCroakDetail(userAction.payload)
        state = STATE.CROAKDETAIL
    elif userAction.action == ACTION.CROAKCREATE:
        createCroak()
    elif userAction.action == ACTION.VOTE:
        voteOnCroak(userAction.payload['croak_id'], userAction.payload['vote'])
    elif userAction.action == ACTION.BACK:
        back()
    elif userAction.action == ACTION.REPLY:
        createCroak(userAction.payload['p_id'])
    else:
        print('something went wrong')
