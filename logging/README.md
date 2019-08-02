
# What is ELK Stack?

![alt text](https://github.com/collabnix/openusm/blob/master/images/elk_stack_overview.png)

# Why we chose ELK?

- ELK is known for its speed and full-text capability
- High Performance indexing over 150GB/hour on all our modern hardware
- It requires smaller RAM – only 1 MB heap
- A Powerful, accurate and efficient search algorithm
- Easy to setup with a single Docker Compose file 
- Powerful query types: phrase queries, wildcard queries, range queries and more fielded searching (e.g. title, author, contents)
- Integrated well with Prometheus which is popular for real-time monitoring


# ELK stack for iDRAC Logs

This builds Elasticsearch, Kibana & Logstash stack running inside Docker container to collect your logs generated out of each container which was used to update your BIOS configuration. 

# How does it work?

Each container runs syslog server out-of-the-box which pushes the logs to ELK stack and hence logs gets captured under Kibana.
There is NO need of any customization to be done to dump the logs under Kibana UI. Everything comes out of the box.
This gives you the ability to analyze any data set by using the searching/aggregation capabilities of Elasticsearch & the visualization power of Kibana.

It is purely based on the official Docker images:

* [elasticsearch](https://github.com/elastic/elasticsearch-docker)
* [logstash](https://github.com/elastic/logstash-docker)
* [kibana](https://github.com/elastic/kibana-docker)

## Pre-requisite


1. Install [Docker](https://www.docker.com/community-edition#/download) version **17.06+**
2. Install [Docker Compose](https://docs.docker.com/compose/install/) version **1.16.0+**
3. Clone this repository

### SELinux

On distributions which have SELinux enabled out-of-the-box you will need to either re-context the files or set SELinux
into Permissive mode in order for docker-elk to start properly. For example on Redhat and CentOS, the following will
apply the proper context:

```bash
$ chcon -R system_u:object_r:admin_home_t:s0 docker-elk/
```

## Usage

### Bringing up the stack

### Pre-requisite:

Ensure that the below syslog driver has been specified:


```
cat /etc/docker/daemon.json
{
  "log-driver": "syslog"
}
root@ubuntu:~#

```

Restart the docker daemon(in case of Ubuntu)

```
service docker restart
```

Building the Elastic Stack first:

```bash
$docker-compose build
```

Start the ELK stack using `docker-compose`:

```bash
$ docker-compose up
```

You can also choose to run it in background (detached mode):

```bash
$ docker-compose up -d
```

Give Kibana about 2 minutes to initialize, then access the Kibana web UI by hitting
[http://localhost:5601](http://localhost:5601) with a web browser.

By default, the stack exposes the following ports:
* 5000: Logstash TCP input.
* 9200: Elasticsearch HTTP
* 9300: Elasticsearch TCP transport
* 5601: Kibana

## Pushing BIOS Configuration Logs from iDRAC to Kibana UI

Try updating the BIOS Token using [this](https://github.com/collabnix/openusm/blob/master/docs/bios-token.md) link.

Open up kibana and you can see that the logs as shown below:

![alt_text](https://github.com/openusm/openusm/blob/master/images/idrac_elk.png)

Want to see it in action?
Refer : [Link](https://youtu.be/jbg4gcp0M8M)


