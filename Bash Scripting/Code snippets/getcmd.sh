#! /usr/bin/env bash

OSTYPE="MSWin"

function SepCmds()
{
      LCMD=${string%%|*}                   # isolate linux command by stripping all chars to the right of the | with %%
      REST=${string#*|}                    # remove the shortest match on the left hence strips the linux command
      WCMD=${REST%%|*}                    # from the remaining value strip all chars to the right of the | with %% so you end up with just the win command 

      
      if [[ $OSTYPE == "MSWin" ]]
      then
         CMD="$WCMD"
      else
         CMD="$LCMD"
      fi
      echo the command selected is: $CMD
}

printf '<systeminfo host="%s" type="%s"' "$HOSTNAME" "$OSTYPE"
printf ' date="%s" time="%s">\n' "$(date '+%F')" "$(date '+%T')"

string="uname -a   |  get-os    |  uname |"

SepCmds $string # note how unlike in python we pass the arg like with a shell command.
