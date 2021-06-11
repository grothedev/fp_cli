#!/bin/bash
#this is the official python CLI program for Frog Pond

import os
import sys
from pathlib import Path
import getopt
import urllib.request
import json
import datetime
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
tStr=''
r=-1
host='http://grothe.ddns.net:8090/api/'
lat=None
lon=None
query=host+"croaks?"
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
opts, extra = getopt.getopt(sys.argv[1:], "hrt:l:ci:");

for o, a in opts:
    if o == '-h':
        print('TODO display help');
        break;
    elif o == '-r': #raw data: don't format; direct API response
        printRaw = True
    elif o == '-i': #get croak by id
        query = host + str(a);
        break;
    elif o == '-c':
        content = input('Type your croak.\n');
        filePath = input('If you would like to attach a file, enter the path. Otherwise leave blank.\n');
        sugTags = ''; #TODO
        tags = input('Enter some tags to which this croak is related.\n');
        #TODO
        break;
    elif o == '-t':
        tStr += a + ',';
    elif o == '-l':
        if a != None:
            query += 'n=' + str(a) + '&';

if tStr != '':
    tStr = ''.join(tStr.split());
    query += 'tags=' + tStr + '&';

res = urllib.request.urlopen(str(query)).read();
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

