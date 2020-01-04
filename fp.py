#!/bin/bash
#this is the official python CLI program for Frog Pond

import os
import sys
from pathlib import Path
import getopt


tStr=''
r=-1
host='localhost:8000/api/'
lat=None
lon=None
query=host+"croaks?"
APPDIR=str(Path.home()) + '/.frogpond/'

print("Welcome to the Pond")

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
    print(o + ', ' + a);
    if o == '-h':
        print('TODO display help');
        break;
    elif o == '-i':
        query = host + str(a);
        break;
    elif o == '-t':
        tStr += a;
    elif o == '-l':
        if a != None:
            query += 'n=' + str(a) + '&';
    elif o == 'c':
        print('creating croak');


print(query);

'''
while getopts :t:l:ci: opt
do
    case $opt in
        i)
            query=$host"croaks/"$OPTARG
            break;
            ;;
        t)
            tStr=$OPTARG
            query=$query"tags="$tStr"&"
            ;;
        l)
            if [[ ! -z $OPTARG ]]
            then
                query=$query"n="$OPTARG
            fi
            ;;
        c)
            echo "creating"
            ;;
    esac

    res="$(curl $query)"
    echo $res
    echo $res > $APPDIR"/res" #saving croaks locally
    #printf %b $res | jq '.[]|.created_at,.content,.tags[].label'
    printf %b $res | jq '.[]' | xargs echo 'yo'
    echo ''
    #printf %b $res | jq '.[].content'
    #echo $res | jq '.[].'

done

echo "Done."
'''
