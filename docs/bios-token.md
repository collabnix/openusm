# How to perform BIOS Token change using OpenUSM

## Pre-requisite:

- [NFS Server](../docs/nfs-setup.md)
- Latest version of Docker Installed (17.06+)
- Python 2.7+ with pip installed

```
$apt install python-pip
$pip install requests
```
- [Sample BIOS token placed under NFS share](../samples/biosconfig.xml)


## Clone the OpenUSM Repository


```
$ git clone https://github.com/openusm/openusm
$ cd openusm
```

## Copy biosconfig.xml file to NFS Share

```
$cp -rf samples/biosconfig.xml /var/nfsshare/
```

## A Quick Look at Script Options

```
$ python bios-token.py --help
usage: bios-token.py [-h] [--verbose] [-i IDRAC] [-n NFS] [-s SHARE]
                     [-c CONFIG] [-f IPS]

Welcome to Universal Systems Manager Bios Token Change

optional arguments:
  -h, --help            show this help message and exit
  --verbose             Turn on verbose logging
  -i IDRAC, --idrac IDRAC
                        iDRAC IP of the Host
  -n NFS, --nfs NFS     NFS server IP address
  -s SHARE, --share SHARE
                        NFS Share folder
  -c CONFIG, --config CONFIG
                        XML File to be imported
  -f IPS, --ips IPS     IP files to be updated
```

## Updating BIOS Token Change for Single System 

```
$python bios-token.py -i <iDRAC-IP> -s /var/nfsshare -c biosconfig.xml -n <NFS-IP>
```

## Updating BIOS Token Change for Multiple System


```
$bios-token.py -f ips.txt -s /var/nfsshare -c biosconfig.xml -n <NFS-IP>
```
where,

ips.txt is a file which includes list of iDRAC IP address. Check out the same file format under [ips.txt](../ips.txt)

## What does this script do?

This script will create as many Docker containers based on number of systems. It means that for every iDRAC IP address, a Docker container will be spun up which does BIOS token change automatically. PLEASE NOTE THAT NO MANUAL REBOOT IS REQUIRED as LC automaticaly handle the job and rebooting the system.

# Troubleshooting

1. The bios-token.py runs well but the container gets exited suddenly

As of now, the IP address has been hard coded into bios-token.py specific to syslog server. Hence, you might need to make changes manually. The fix will be provided ASAP.


