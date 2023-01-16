
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

## Conditionals examples

```bash
if ls | grep .txt > /dev/null # dont show the output of this command
then
	echo "these .txt files have been found:"
	ls -l | grep .txt
	count=$(ls -l | grep .txt | wc -l)
	echo "number of .txt files found: $count"
else
	echo "no text files found"
fi
```

### to make comparisons like this you have to enclose them in [[ ]]

```bash
num1=10
num2=2
if [[ $num1 -eq $num2 ]] ; then echo "num1 matches num2" ; fi

# create a test.txt in the parent dir to test
```bash
if [[ -e ../test.txt ]] ; then echo "test.txt exists" ; fi
```

### demonstrate the  difference between using (( )) vs [[ ]]

```bash
if  [[ $num1 > $num2 ]]
then
	echo "$num1 is larger than $num2"
else 
	echo "$num1 is smaller than $num2"
fi 

if  (( $num1 > $num2 ))
then
	echo "$num1 is larger than $num2"
else 
	echo "$num1 is smaller than $num2"
fi
```

### Shorten your code example

```bash
DIR="/home/sen"

if [[ -d $DIR ]]
then
	ls $DIR
else
	echo "this directory does not exist"
fi

echo "and now the same result with shorter code: "

[[ -d $DIR ]] && ls $DIR || echo "this directory does not exist"
```


## Looping

### use (( )) when evaluating numerical values

```Bash
i=0
while (( i < 10 ))
do
	echo $i
	let i++
done
```
### to see what this does just pas a few arguments when calling this script
```Bash
for ARG ; do echo "here is an argument: $ARG" ; done

for value in list_item1 list_item2 list_item3
do
	echo $value
done
```
### List all .txt files and pass them into a for loop

```Bash

for value in $(ls | grep .txt) ; do echo $value; done
```

-q exists with the zero status (success) without displaying output
so while the statement that there is a file containing txt is true
the commands between do and done will be executed

```Bash
while ls | grep -q txt
do
	echo -n "there is a file with txt in its name here: ";
	pwd;
	echo "deleting .txt files";
	rm -f *.txt;
	cd ..;
done
```
### loop over a range

```Bash
for x in {0..10..2}
do
	echo $x
done
```

### while read 

```Bash
# Read file line per line we can replace certain chars with "/" e.g. /_/- replaces underscores with hyphens.
# // replace all instances for each line read

cat logfile | while read logentry
do
	echo "This is a logentry:${log//_/-}"
done

# Can also be written in a oneliner:
cat logfile | while read log; do echo "This is a logentry:${log//_/-}"; done
```

## REGEX

### Capture groups

The =~ binary operator provides the ability to compare a string to a POSIX extended regular expression in the shell.

```Bash
info=$(ifconfig)
if [[ "$info" =~ .+(172\.31\.27\.137).+$ ]]
then
    result= "$(ping -c 5 -n4 ${BASH_REMATCH[1]})" && echo $result
fi
```

### Capture groups with IP address patterns

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

## Working with filesystems 

Use the following commands to list the files created on today with the .zip extension:  

```Bash
ls /tmp  -ltr | grep "`date | awk '{print $2" "$3}'`" | grep .zip
```