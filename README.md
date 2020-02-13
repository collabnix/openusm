# Open Universal Systems Manager

![alt text](https://github.com/collabnix/openusm/blob/master/images/openusm_logo.png)

A modern approach to Server Management, Insight Logs Analytics and Machine Learning solution integrated with monitoring & logging pipeline using Docker, Redfish, Prometheus & [ELK Stack](https://github.com/openusm/openusm/tree/master/logging).

# Highlights

- OpenUSM is a suite of open source tools/scripts which purely uses Redfish API to perform Server Management tasks & Insight Log Analytics using Dockerized ELK Stack.
- OpenUSM can be bundled as Docker Images which is lightweight, stand-alone, executable package of a piece of software that includes everything needed to run it: code, runtime, system tools, system libraries, settings. Hence, no need of host dependencies packages
- OpenUSM is an out-of-band system management solution purely based on Redfish API Interface.
- It is a platform agnostic solution(can be run from laptop, server or cloud) and works on any of Linux or Windows platform with Docker Engine running on top of it.
<br></br>

![alt text](https://github.com/collabnix/openusm/blob/master/images/kibana_openusm.png)
<p>    ------------------- Kibana visualizing Pie-Chart for LC logs collected over the last 1 year time period--------------------</p>

# Value Proposition

- OpenUSM architecture can scale both vertically & horizontally
- OpenUSM architecture can be easily integrated and extended with 3rd party open source tools.(example - the choice of InfluxDB instead of Prometheus as monitoring tool, using 3rd Party logging tool instead of ELK stack etc.)
- OpenUSM bundle can be built and customized by anyone based on the needs and holds a plug-and-play components and functionalities.
- OpenUSM can easily be integrated with Chef/Ansible/Puppet for automating the Server Management tasks/operations.

# Architecture

![alt text](https://github.com/collabnix/openusm/blob/master/images/openusm_technology_overview.png)

# How openUSM works?

OpenUSM uses "Container-Per-Server(CPS)" model. For each server management tasks, there are Python-scripts which when executed builds and run Docker containers, uses Redfish API to communicate directly with Dell iDRAC, collects iDRAC/LC logs and pushes it to ELK(Elasticsearch, Logstash & Kibana) stack for further log analytics.For n-number of Dell Servers, the overall iDRAC/LC logs gets collected to centralized ELK stack which again runs as Microservices inside Docker containers. One can easily see iDRAC logs under Kibana UI. OpenUSM uses Prometheus Stack for monitoring System components like GPU/CPU monitoring using NVIDIA-DOCKER & Node Exporter. 



![openusm](https://github.com/collabnix/openusm/blob/master/images/openusm_workflow.png)


# Getting Started with OpenUSM

## Quick Guide

[Getting Started with OpenUSM on Docker for Windows Platform](http://collabnix.com/getting-started-with-openusm-on-docker-for-windows-platform/)<br>


To get started with OpenUSM on Linux Platform, we have built bootstrapping scripts for you to keep it simple and quick. 

Pre-requisite:

- Install Python on Linux System
- Ensure that you have enough space for containers to run(recommended 10GB of space)
- Ubuntu or Debian based OS

## Installing Docker & Docker Compose


Cloning the Repository

``` 
$git clone https://github.com/openusm/openusm
```

Bootstrapping Docker

If you have Docker already installed on your system, you can skip this step. If not, run the below command to install Docker & Docker Compose on your system.

 ```
 $sh bootstrap.sh install_docker
```

Ensure that ```curl```package is already installed on this system.



## Manual Method:

Preparing Your System

[Ubuntu](docs/os/ubuntu-installation.md) <br>
[Debian](docs/os/debian-installation.md) <br>
[CentOS](docs/os/centos-installation.md) <br>
[RHEL](docs/os/rhel-installation.md) <br>

# Bootstrapping Elastic Stack

OpenUSM is 100% containerized solution and hence we will be running ELK inside Docker containers. To keep it simple, we designed a docker-compose file which can get you started in a matter of seconds. 

Before you initiate ELK stack , ensure that you set the vm.max_map_count kernel setting needs to be set to at least 262144 for Linux system

```
sudo sysctl -w vm.max_map_count=262144
```

Execute the same bootstrap file with provision-elk argument to bring up ELK stack as shown below:

 ```
 $sh bootstrap.sh provision_elk
```

Just wait for 30-40 seconds to get ELK stack up and running.



## Configuring syslog service for Docker daemon

To allow H/W logs generated to be dispatched to logstash, we would need syslog driver configured within Docker daemon. This is how to achieve that. Open /etc/docker/daemon.json and add the below entry:

```
{
  "log-driver": "syslog"
}
```

Restart the Docker Daemon

```
service docker restart
```

OpenUSM is a suite of tools and utilities which configures and manage the lifecycle of system management. OpenUSM has a capability to perform the following functions:

[BIOS Token Change](docs/bios-token.md) <br>
[Firmware Update](docs/firmware.md)<br>
[Pushing iDRAC Logs to ELK Stack](docs/idrac2elk.md)<br>
[Pushing LC logs to ELK Stack](docs/lc2elk.md)<br>
[Pushing Sensors Logs to ELK Stack](docs/sensors2elk.md)<br>


## Blogs

[Introducing OpenUSM](http://en.community.dell.com/techcenter/systems-management/w/wiki/12502.introducing-openusm-simplifying-server-management-insight-log-analytics-using-docker-containers)<br>
[OpenUSM - Let Containers Manage Your datacenter](http://collabnix.com/introducing-openusm-simplifying-server-management-insight-log-analytics-using-docker-containers/)<br>

## Webinars

[Online Webinar on OpenUSM](https://www.slideshare.net/ajeetraina/collabnix-online-webinar-integrated-log-analytics-monitoring-using-docker-elastic-stack)


## Roadmap ahead

Refer [Report](https://github.com/openusm/openusm/tree/master/reports) section to track what new features and improvement are coming next in OpenUSM.

# How do I become a contributor?

We invite new contributors to contribute towards this project repository. We would also ask you to propose any improvements or contributions for future releases.

# Quick Videos/ Resources

[![Pushing iDRAC Logs to ELK Stack](https://github.com/collabnix/openusm/blob/master/images/idrac_elk_logs.png)](https://www.youtube.com/watch?v=jbg4gcp0M8M)
