import pandas
import csv
 
 
# Convert JSON data to CSV with the pandas library
# Bash style file path

import pandas as pd

with open('rootdir/subdir/myinputfile.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)

df.to_csv('myoutputfile.csv', encoding='utf-8', index=False)
