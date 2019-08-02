## Using Traditional Method

## Installing NFS 

```
$apt install nfs-kernel-server
```

## Configuring NFS file

```
$cat /etc/exports
/var/nfsshare   *(rw,sync,no_root_squash,no_all_squash)```

##  Starting the NFS service

```
$systemctl restart nfs-kernel-server
```
## Using Docker Containers

[tbd]
