#! /usr/bin/env bash
# NOTE: IFS is required or else spaces in array elements mess up the script
# Find files in dirs that have been modified since x days

IFS=""
mydirs=("/c/Users/Public/"
"/c/Documents and Settings/Default"
"/c/Users/Default")
eventid='4657'
regkey=$(reg query 'HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run')
days=24

mkdir -p ./modified

for dir in "${mydirs[@]}"
do
    echo "searching for modified files in: ${dir}"
    find "${dir}" -type f -mtime -$days -exec cp '{}' ./modified \;
done

printf "\nfollowing executables were found in startup: \n"

for entry in "${regkey[@]}"
do
    echo "${entry}" | sed -e 's/^[[:space:]]*//' | cut -d' ' -f1
done

