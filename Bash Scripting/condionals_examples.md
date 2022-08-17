# Conditionals examples
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
