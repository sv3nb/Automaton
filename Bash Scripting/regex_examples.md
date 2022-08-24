# Capture groups

The =~ binary operator provides the ability to compare a string to a POSIX extended regular expression in the shell.

```Bash
info=$(ifconfig)
if [[ "$info" =~ .+(172\.31\.27\.137).+$ ]]
then
    result= "$(ping -c 5 -n4 ${BASH_REMATCH[1]})" && echo $result
fi
```

# Capture groups with IP address patterns
<b>Note</b>:
The expressions such as '\s', '\d' etc... are not supported!

```Bash
if [[ "this is the first IP 10.15.10.1 and this the second IP 10.15.10.2" =~ \
 ^.*[[:space:]]([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*[[:space:]]([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})$ ]]
then 
    echo "${BASH_REMATCH[1]}"
    echo "${BASH_REMATCH[2]}"
fi


```
