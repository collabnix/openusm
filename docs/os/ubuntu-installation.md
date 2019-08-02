# Installing Docker and Docker-Compose on Ubuntu 16.04

## Run the below command to install Docker 

```
curl -sSL https://get.docker.com/ | sh
```

## Run this command to download the latest version of Docker Compose:

```
curl -L https://github.com/docker/compose/releases/download/1.19.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
```

## Apply executable permissions to the binary:

```
chmod +x /usr/local/bin/docker-compose
```

## Test the installation

```
docker-compose version
```
