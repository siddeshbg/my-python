# FileCompare
A simple script to look for items found in source file, but missing in destination.

This script takes two files each containing some data. Then it looks for each line in source, whether it is present in
destination. In the end it gives summary of total lines in source, destination, count of missing lines and actual 
missing items

## Usage
```aidl
./src/FileCompare.py 
usage: FileCompare.py [-h] -s SRC -d DEST

Script to look for items found in source file, but missing in destination

optional arguments:
  -h, --help            show this help message and exit
  -s SRC, --src SRC     Source file
  -d DEST, --dest DEST  Destination file

```

## Example
```aidl
src/FileCompare.py -s ../tests/resources/src.txt -d ../tests/resources/dest.txt
******************************
		Statistics
******************************
Total items in source: 41
Total items in destination: 34
Missing in destination: 7
['15476', '15481', '15483', '15488', '15499', '15526', '15535']
```