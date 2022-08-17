#! /usr/bin/env bash


# Looping

## use (( )) when evaluating numerical values

i=0
while (( i < 10 ))
do
	echo $i
	let i++
done

## to see what this does just pas a few arguments when calling this script

for ARG ; do echo "here is an argument: $ARG" ; done

for value in list_item1 list_item2 list_item3
do
	echo $value
done

## List all .txt files and pass them into a for loop

for value in $(ls | grep .txt) ; do echo $value; done


-q exists with the zero status (success) without displaying output
so while the statement that there is a file containing txt is true
the commands between do and done will be executed

while ls | grep -q txt
do
	echo -n "there is a file with txt in its name here: ";
	pwd;
	echo "deleting .txt files";
	rm -f *.txt;
	cd ..;
done

# loop over a range

for x in {0..10..2}
do
	echo $x
done
