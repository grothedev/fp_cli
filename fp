#!/bin/bash
#this is the official CLI program for Frog Pond


tStr=''
r=-1
host='localhost:8000/api/'
lat=null
lon=null
query=$host"croaks?"
APPDIR=~/.frogpond/

echo "Welcome to the Pond"

if [ ! -d "$APPDIR" ]; then
    mkdir $APPDIR
fi

#get command, make api request, present formatted results

while getopts :t:l:ci: opt
do
    case $opt in
        i)
            query=$host"croaks/"$OPTARG
            break;
            ;;
        t)
            tStr=$OPTARG
            query=$query"tags="$tstr"&"
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
    cat res > $APPDIR"/res" #probably should save croaks locally
    cat res | jq '.[].content'
    cat res | jq '.[].id'
done


echo "Done."
