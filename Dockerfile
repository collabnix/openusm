FROM python:2.7
MAINTAINER "Ajeet S Raina" <Ajeet_Raina@dell.com>

RUN apt-get update -y && \
    apt-get install -y git python-pip 
RUN pip install requests
ADD . /redfish
#RUN git clone https://github.com/ajeetraina/redfish
WORKDIR /redfish

