#! /usr/bin/env bash

reg export "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" $(hostname)_hlkm.bak

# you can check the exact encoding used for a file with this command
# next command converts between utf formats

filetype=$(file -bi "./$(hostname)_startup.bak")
if [[ $filetype =~ "utf-16" ]]
then
    echo "its a utf-16 file" && iconv -f utf-16 -t utf-8 "./$(hostname)_startup.bak" | grep -E '.*whateveryouwanttofind.*' -B1
elif [[ $filetype =~ "utf-8" ]]
then
    echo "its a utf-8 file" && grep -E -B1 '.*whateveryouwanttofind.*' "./$(hostname)_startup.bak"

fi