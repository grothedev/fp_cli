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

#TODO check last query time? or add option for cached croaks?
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
