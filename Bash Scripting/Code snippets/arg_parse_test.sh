#! /usr/bin/bash

TGZ=0
if (( $# > 0 ))
then
    if [ ${1} == '-z' -o ${2} == '-z' ] # if the first OR second argument passed to the scripped equals '-z'
    then 
        TGZ=1
        shift
    fi
fi
echo $TGZ