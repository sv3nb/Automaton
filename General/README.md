# General

Some general purpose code that you can use in any script.


### Logging
```
from pathlib import Path
import logging
import os
import gzip, shutil

if not os.path.exists('.\log'):
    os.makedirs('.\log')

logfile = ".\log\mylog"
logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger()
```

### Find .gz file and unzip
```
logger.info(f"Start script: find gz file and unzip")

currentdir = os.getcwd()
for path in Path(currentdir).rglob('*.gz'):
  zippedfile = path.name
with gzip.open(zippedfile, 'r') as f_in, open(zippedfile.strip('.gz'), 'wb') as f_out:
  shutil.copyfileobj(f_in, f_out)
  syslogfile = f_out.name
  ```
