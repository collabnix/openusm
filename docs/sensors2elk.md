# Sending DellEMC Hardware Sensor logs to ELK Stack Made Easy using Docker & Redfish

## Pre-requisite:

- Install Linux (Tested on Ubuntu 16.04) as VM or Bare Metal OS
- Install Python using ```apt-get install python```


## Cloning the Repository

```
git clone https://github.com/openusm/openusm
cd openusm
```

## Installing Docker & Docker Compose

```
sh bootstrap.sh provision_docker
```

## Configuring Syslog Server for Docker Daemon

Open/Create /etc/docker/daemon.json and add the below lines:

```
{
  "log-driver": "syslog"
 
}
```

Restart the Docker daemon

```
service docker restart
```

## Installing ELK Stack

```
sh bootstrap.sh provision_elk
```

Verify the Kibana UI by opening ```http://<IP>:5601``` under the browser.
You can also verify using the below commands:

```
curl <HOSTIP>:9200
curl <HOSTIP>:5601
```

## Sending LC logs to ELK Stack

```
cd openusm/logging/logextractor
python sensorlogexporter.py -i <iDRACIP>  -ei <ElasticIP> -eu elastic -ep changeme
```

## Open Kibana UI and search for Index by name "lc_index"

Click on Discovery option on the left side to view the logs.

## Visualization through Kibana UI

## Search Index Pattern(fan_index)
<br>

![alt text](https://github.com/openusm/openusm/blob/master/images/fan1.png)<br>



![alt text](https://github.com/openusm/openusm/blob/master/images/fan2.png)<br>
<br>
