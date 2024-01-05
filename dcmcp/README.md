# dcmcp

## What is it?
A commandline application to copy DICOM files from a directory to another directory by PatientID.

## Usage

```shell
usage: dcmcp [-h] -i INPUT -o OUTPUT --id ID [-v]

Copy DICOM files for a specific patient from one directory to another.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input directory
  -o OUTPUT, --output OUTPUT
                        Output directory
  --id ID               Patient ID
  -v, --verbose         Output directory 
```