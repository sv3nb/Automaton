show attributes for each file found, filter on files starting with A (archive attrib) and .log in the string
finally only show the file path by slicing on char position, sed will trim any leading whitespace to clean up output.
(depending on attrib version the number of spaces can change)

```Bash
find ./ -name '*.sh' -exec attrib {} \; | egrep '^A.*log.*$' | cut -c22- | sed -e 's/^[[:space:]]*//'
```

find files with size larger than 5GB, suppress 'permission denied' errors, show top 5

```Bash
find $SYSTEMROOT -size +5G 2>/dev/null | head -5 
```

For Windows: get net shares, strip all spaces and additional info and store the dirs in a var

```Bash
dirs=$(net share | grep 'C:' | cut -d'$' -f2 | sed -e 's/^[[:space:]]*//' | cut -d' ' -f1)

for share in $dirs
do
    echo "recently modified files of $share:"
    find $share -mtime -1
    printf "\n"
done
```