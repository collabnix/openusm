# How to send DellEMC LifeCycle Controller logs to ELK Stack

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
python lclogexporter.py -i <iDRACIP>  -ei <ElasticIP> -eu elastic -ep changeme
```

## Open Kibana UI and search for Index by name "lc_index"

Click on Discovery option on the left side to view the logs.

## Visualization through Kibana UI

## Search Index Pattern(lc_index)
<br>

![alt text](https://github.com/openusm/openusm/blob/master/images/lclogexporter1.png)<br>

## Click Next for Step 2

![alt text](https://github.com/openusm/openusm/blob/master/images/logextporter2.png)<br>

## Configuring Time Filter Settings
<br>
<br>

![alt text](https://github.com/openusm/openusm/blob/master/images/lclogexporter3.png)<br>
<br>
<br>

## Listing Fields under Index Pattern

![alt text](https://github.com/openusm/openusm/blob/master/images/lclogexporter4.png)<br>
<br>
<br>

## Discovering the Logs

![alt text](https://github.com/openusm/openusm/blob/master/images/lclogexporter5.png)<br>
<br>
<br>

![alt text](https://github.com/openusm/openusm/blob/master/images/lclogexporter6.png)<br>
<br>
<br>

![alt text](https://github.com/openusm/openusm/blob/master/images/lclogexporter7.png)<br>
<br>
<br>

## Displaying Pie-Chart


![alt text](https://github.com/openusm/openusm/blob/master/images/lclogexporter11.png)<br>
<br>
<br>
