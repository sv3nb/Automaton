#! /usr/bin/bash
# usage: "winlogs.sh -z dir"

TGZ=0
if (( $# > 0 ))
then
    if [[ ${1:0:2} == '-z' ]] # if the argument passed to the scripped equals '-z'
    then 
        TGZ=1
        shift # shifts the argument out of the way 
    fi
fi
SYSNAM=$(hostname)
LOGDIR=${1:-1/tmp/${SYSNAM}_logs} 
# due to the -z being shifted out of the way this now becomes the first arg '$1'
# the ':-1/tmp..' is to provide a default value in case the user does provide one when calling the script.

mkdir -p $LOGDIR
cd ${LOGDIR} || exit -2

wevtutil el | while read ALOG
do
    ALOG="${ALOG%$'\r'}"				# <6>
    echo "${ALOG}:"					# <7>
    SAFNAM="${ALOG// /_}"				# <8>
    SAFNAM="${SAFNAM//\//-}"
    wevtutil epl "$ALOG" "${SYSNAM}_${SAFNAM}.evtx"
done

if (( TGZ == 1 ))					# <9>
then
    tar -czvf ${SYSNAM}_logs.tgz *.evtx			# <10>
fi