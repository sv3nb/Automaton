#! /usr/bin/env bash
if type -t scutil $> /dev/null
then 
    os=macOS
elif type -t wevtutil &> /dev/null
then
    os=MSWin
else
    os=Linux
fi
echo $os


