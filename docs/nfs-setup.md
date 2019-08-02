# Configuring NFS Server 

[Debian](docs/nfs/debian) <br>
[CentOS](docs/nfs/centos) <br>
[Windows](docs/nfs/windows)<br>
[RHEL](docs/nfs/rhel)<br>
[Ubuntu](docs/nfs/ubuntu)

## Using Traditional Method

## Installing NFS 

```
$apt install nfs-kernel-server
```

## Configuring NFS file

```
$cat /etc/exports

/var/nfsshare   *(rw,sync,no_root_squash,no_all_squash)
```

##  Starting the NFS service

```
$systemctl restart nfs-kernel-server
```

## Using Docker Containers

[tbd]
