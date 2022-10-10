
# Bash reference GNU

## Internal variables

```Bash

- Double quote your vars when referencing them.
- {} should be used when appending something to the var value
e.g. "${myvar}somestring"

$BASH_VERSINFO
$HOME
$HOSTNAME
$#  = number of positional parameters passed to a script or function
$!  = Pid of the last command processed
$$  = id of the process that executed Bash
$MACHTYPE = shows OS & Hardware info
$PATH = Search path
$* = returns all positional parameters in a single string
$_ = Outputs the last field from the last command executed
$@  = expands all cli args as separate words and allows you to loop over them
```
