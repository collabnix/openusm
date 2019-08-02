import requests
import json
import sys
import re
import time
import os
import warnings


from elasticsearch import Elasticsearch
from datetime import datetime



try:
    idrac_ip = os.environ['IDRAC_IP']
    idrac_username = os.environ['IDRAC_USERNAME']
    idrac_password = os.environ['IDRAC_PASSWORD']

    elastic_ip = os.environ['ELASTIC_IP']
    elastic_username = os.environ['ELASTIC_USERNAME']
    elastic_password = os.environ['ELASTIC_PASSWORD']

    es = Elasticsearch([elastic_ip],
                       http_auth=(elastic_username, elastic_password),
                       scheme="http",
                       port=9200,
                       )
except Exception as e:
    print("- FAIL: You must pass in script name along with iDRAC IP / iDRAC username / iDRAC password")
    sys.exit(0)



def getSystemName():
    response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/Bios' % idrac_ip, verify=False,
                            auth=(idrac_username, idrac_password))
    data = response.json()
    system_name = data[u'Attributes']['SystemModelName']
    return (system_name)


# Function to get lifecycle logs (LC)
def getJSONResponse(next_url):
    response = requests.get('https://%s%s' % (idrac_ip, next_url), verify=False, auth=(idrac_username, idrac_password))
    data = response.json()

    return data



def get_thermal_info():
    system_name = getSystemName()

    print(system_name)
    temp_dict = {}
    data = getJSONResponse('/redfish/v1/Chassis/System.Embedded.1/Thermal')
    id_ts = time.time()
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    for i in data[u'Temperatures']:
        temp_dict = {}
        id_ts = time.time()
        temp_dict[u'Idrac_Ip'] = idrac_ip,
        temp_dict[u'Server_Model'] = system_name,
        temp_dict[u'Created'] = ts
        temp_dict[u'MemberId'] = i[u'MemberId']
        temp_dict[u'MinReadingRangeTemp'] = i[u'MinReadingRangeTemp']
        temp_dict[u'Name'] = i[u'Name']
        temp_dict[u'PhysicalContext'] = i[u'PhysicalContext']
        temp_dict[u'ReadingCelsius'] = i[u'ReadingCelsius']
        temp_dict[u'Health'] = i[u'Status']['Health']
        temp_dict[u'State'] = i[u'Status']['State']
        temp_dict[u'UpperThresholdCritical'] = i[u'UpperThresholdCritical']
        temp_dict[u'UpperThresholdFatal'] = i[u'UpperThresholdFatal']

        es.create(index='temp_index', doc_type='temp_doc_' + str(idrac_ip), id=int(id_ts), body=temp_dict)
        time.sleep(3)


    return temp_dict


def get_fans_info():

    system_name = getSystemName()

    print(system_name)
    fan_dict = {}
    data = getJSONResponse('/redfish/v1/Chassis/System.Embedded.1/Thermal')

    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    for i in data[u'Fans']:
        fan_dict = {}

        id_ts = time.time()
        fan_dict[u'Idrac_Ip'] = idrac_ip,
        fan_dict[u'Server_Model'] = system_name,
        fan_dict[u'Created'] = ts
        fan_dict[u'FanName'] = i[u'FanName']
        fan_dict[u'LowerThresholdCritical'] = i[u'LowerThresholdCritical']
        fan_dict[u'LowerThresholdFatal'] = i[u'LowerThresholdFatal']
        fan_dict[u'LowerThresholdNonCritical'] = i[u'LowerThresholdNonCritical']
        fan_dict[u'MaxReadingRange'] = i[u'MaxReadingRange']
        fan_dict[u'MinReadingRange'] = i[u'MinReadingRange']
        fan_dict[u'Name'] = i[u'Name']
        fan_dict[u'PhysicalContext'] = i[u'PhysicalContext']
        fan_dict[u'Reading'] = i[u'Reading']
        fan_dict[u'ReadingUnits'] = i[u'ReadingUnits']
        fan_dict[u'Health'] = i[u'Status']['Health']
        fan_dict[u'State'] = i[u'Status']['State']
        fan_dict[u'MemberId'] = i[u'MemberId']

        es.create(index='fans_index', doc_type='fans_doc_' + str(idrac_ip), id=int(id_ts), body=fan_dict)
        time.sleep(3)

    return fan_dict



while(True):

    get_thermal_info()
    time.sleep(5)
    get_fans_info()
    time.sleep(5)
