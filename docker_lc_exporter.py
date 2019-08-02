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


def get_LC_logs():
    try:
        es.indices.delete(index='lc_index', doc_type='lc_doc'+str(idrac_ip))
    except Exception as e:
        pass

    columns = [
        'Idrac_Ip',
        'Server_Model',
        'Created',
        'Description',
        'EntryType',
        'Id',
        'Message',
        'MessageID',
        'Name',
        'OemRecordFormat',
        'Severity']

    system_name = getSystemName()

    print(system_name)

    data = getJSONResponse('/redfish/v1/Managers/iDRAC.Embedded.1/Logs/Lclog')

    try:

        while (data[u'@odata.nextLink'] != None):

            time.sleep(2)
            print(data[u'@odata.nextLink'])

            for i in data[u'Members']:
                print("%s : %s" % ('Id', i[u'Id']))

                data_dict = {
                    'Idrac_Ip': idrac_ip,
                    'Server_Model': system_name,
                    'Created': i[u'Created'],
                    'Description': i[u'Description'],
                    'EntryType': i[u'EntryType'],
                    'Id': i[u'Id'],
                    'Message': i[u'Message'],
                    'MessageID': i[u'MessageID'],
                    'Name': i[u'Name'],
                    'OemRecordFormat': i[u'OemRecordFormat'],
                    'Severity': i[u'Severity'],

                }
                #                 df.loc[len(df)] = data_dict
                es.create(index='lc_index', doc_type='lc_doc'+str(idrac_ip), id=str(i[u'Id']), body=data_dict)

            print("#" * 100)
            time.sleep(2)

            data = getJSONResponse(data[u'@odata.nextLink'])

    except KeyError as e:

        print("Error:", e)
        print(dir(e))

        for i in data[u'Members']:
            data_dict = {

                'Idrac_Ip': str(idrac_ip),
                'Server_Model': system_name,
                'Created': i[u'Created'],
                'Description': i[u'Description'],
                'EntryType': i[u'EntryType'],
                'Id': i[u'Id'],
                'Message': i[u'Message'],
                'MessageID': i[u'MessageID'],
                'Name': i[u'Name'],
                'OemRecordFormat': i[u'OemRecordFormat'],
                'Severity': i[u'Severity'],

            }
            #             df.loc[len(df)] = data_dict
            es.create(index='lc_index', doc_type='lc_doc'+str(idrac_ip), id=str(i[u'Id']), body=data_dict)

            print("%s : %s" % ('Id', i[u'Id']))

    return




get_LC_logs()


