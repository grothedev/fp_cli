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
#########################



#########################
# FUNCTIONS #
###

#shows a croak in a pretty way
def displayCroak(c):
    print('Croak ' + str(c['id']) + ': ' + c['created_at']);
    print('  ' + c['content']);
    print('  Tags: ' + c['tags_str']);
    print();

#assoc human-readable timestamp, tag list, etc.
def formatData(c):
    ts = '';
    for t in c['tags']:
        ts += t['label'] + ', ';
    ts = ts[:len(ts)-2]; #remove extra comma
    c['tags_str'] = ts;

    #c['timestamp'] = datetime.datetime.strptime(c['created_at'], '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d at %H:%M');

##########################

##########################
# GLOBAL VARS #
###
tagsStr=''
tagsExclusive=False
r=-1
apiurl='http://grothe.ddns.net:8090/api/'
lat=None
lon=None
query=apiurl+"croaks?"
APPDIR=str(Path.home()) + '/.frogpond/'
printRaw=False
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


#get command, make api request, present formatted results

#TODO check last query time? or add option for cached croaks?


###
# INPUT PARSING #
###
opts, extra = getopt.getopt(sys.argv[1:], "hrt:l:m:ci:");

for o, a in opts:
    if o == '-h':
        print('TODO display help');
        break;
    elif o == '-r': #raw data: don't format; direct API response
        printRaw = True
    elif o == '-i': #get croak by id
        query = apiurl + 'croaks/' + str(a);
        break;
    elif o == '-c': #create a croak
        content = input('Type your croak.\n');
        filePath = input('If you would like to attach a file, enter the path. Otherwise leave blank.\n');
        sugTags = ''; #TODO
        tags = input('Enter some tags to which this croak is related.\n');
        re.sub(' ', ',', tags) #replace spaces with commas for API compat
        postData = {
            'content': content,
            'tags': tags,
            'x': 0, 'y': 0, #TODO location
        }
        resp = None
        if filePath != None and filePath != '':
            filesData = {'f': ('f', open(filePath, 'rb'))}
            headers = {'content-type': 'multipart/form-data'}
            resp = requests.post(apiurl+'croaks', data=postData, files=filesData, headers=headers)
        else:
            resp = requests.post(apiurl+'croaks', data=postData)
        print(resp.text)
        
        #this is the only special case where we make a POST request. 
        #the request has already been made and feedback outputted to user, so we will exit program.
        sys.exit(0)
        break;
    elif o == '-m': # "mode". exclusive or inclusive tags
        if a != 0:
            tagsExclude = True
    elif o == '-t': # specify tags
        tagsStr = a
        re.sub(' ', ',', tagsStr)
        print('Gathering croaks which contain ' + tagsExclude ? 'all' : 'any' + ' of the following tags: ' + tagsStr.split(','))
    elif o == '-l': # limit number of results
        if a != None:
            query += 'n=' + str(a) + '&';

if tagsStr != '':
    query += 'tags=' + tagsStr + '&';

resp = requests.get(str(query)).read();
croaks = json.loads(res);


###
# OUTPUT #
###

if printRaw:
    print(res.decode('utf-8'))
else:
    print("~   ~  ~~ ~~~~~ ~~  ~   ~\nWelcome to the Pond!\n")
    for c in croaks:
        formatData(c);
        displayCroak(c);
    print("~   ~  ~~ ~~~~~ ~~  ~   ~");

