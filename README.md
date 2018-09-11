# takehome_datadownloader
A program that can be used to download data from multiple sources and protocols to local disk.

##### Current supported protocols
- http, https, ftp, sftp

## Installation
 `python setup.py install`


## How to use
First, list the target URL to be downloaded in the input text file.
For example 'urls.txt' may contain the following URL.

```
ftp://speedtest:speedtest@ftp.otenet.gr/test10Mb.db
http://speedtest.ftp.otenet.gr/files/test100k.db
http://speedtest.ftp.otenet.gr/files/test10Mb.db
```

If it required username and password to download a file.
Please specify them in the URL as the example below.

ftp://user:password@speedtest.com/dir/file2.txt', 'file2.txt

To download the file from these URL to "downloaded_sources/" use the command below.

`datadownloader -u urls.txt -o downloaded_sources/`


## How to uninstall
`python setup.py install --record files.txt`

`cat files.txt | xargs rm -rf`

## How to run unit test
Go to package root directory then run test cases using pytest

1.`cd takehome_datadownloader/`

2.`pytest`