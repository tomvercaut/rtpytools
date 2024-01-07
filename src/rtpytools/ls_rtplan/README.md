# ls_rtplan

## What is it?
A commandline application to list the RTPLAN DICOM files in a directory. 

The application creates a tabular layout with the following info:
* filename \[limited to 40 characters\]
* patient ID
* patient name
* plan name
* plan label

## Usage

```shell
usage: ls_rtplan [-h] [-d DIR] [-p PREFIX] [-l LIMIT]

Print an overview of the RTPLANs in a directory.

options:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Path to the directory.
  -p PREFIX, --prefix PREFIX
                        Prefix of the RTPLAN files.
  -l LIMIT, --limit LIMIT
                        Limit the number of RTPLANs to list.
```