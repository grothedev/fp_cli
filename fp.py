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

#shows a croak in a pretty way
def displayCroak(c):
    print('Croak ' + str(c['id']) + ': ' + c['timestamp']);
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

    c['timestamp'] = datetime.datetime.strptime(c['created_at'], '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d at %H:%M');
##########################


tStr=''
r=-1
host='http://127.0.0.1:8000/api/'
lat=None
lon=None
query=host+"croaks?"
APPDIR=str(Path.home()) + '/.frogpond/'
###########################



print("~   ~  ~~ ~~~~~ ~~  ~   ~\nWelcome to the Pond!\n")

if not os.path.isdir(APPDIR):
    if not os.path.exists(APPDIR):
        os.mkdir(APPDIR);
        print("Made app directory " + APPDIR);
    else:
        print("Error: another file exists at " + APPDIR);


#get command, make api request, present formatted results

#TODO check last query time? or add option for cached croaks?



opts, extra = getopt.getopt(sys.argv[1:], "ht:l:ci:");

for o, a in opts:
    if o == '-h':
        print('TODO display help');
        break;
    elif o == '-i':
        query = host + str(a);
        break;
    elif o == 'c':
        print('creating croak');
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

for c in croaks:
    formatData(c);
    displayCroak(c);

print("~   ~  ~~ ~~~~~ ~~  ~   ~");
