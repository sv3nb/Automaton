#! /usr/bin/env bash
# simple script to check if logging is enabled for specific eventlog

seclogs=$(wevtutil el | grep -i security)
eventlog="Netlogon/Operational"

for log in $seclogs
do 
    log_state=$(wevtutil gl $log)
    if [[ $log_state =~ "enabled: true" ]]
    then
        echo "$log is enabled"
    else
        if [[ $log_state =~ "The specified channel could not be found" ]]
        then
            continue
        else 
            printf "$log is disabled!"
        fi
    fi
done
