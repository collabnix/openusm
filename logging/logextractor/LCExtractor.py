
# GetIdracLcLogsREDFISH. Python script using Redfish API to get iDRAC LC logs.
#
# _author_ = Texas Roemer <Texas_Roemer@Dell.com>
# _version_ = 1.0
#
# Copyright (c) 2017, Dell, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#

import requests
import json
import sys
import re
import time
import os
import warnings
from elasticsearch import Elasticsearch
from datetime import datetime

warnings.filterwarnings("ignore")

try:
    idrac_ip = '100.98.24.105'
    idrac_username = 'root'
    idrac_password = 'calvin'
    es = Elasticsearch(['100.98.26.181'],
                       http_auth=('elastic', 'changeme'),
                       scheme="http",
                       port=9200,
                       )


except:
    print("- FAIL: You must pass in script name along with iDRAC IP / iDRAC username / iDRAC password")
    sys.exit()

try:
    os.remove("lc_logs.txt")
    # os.remove("lc_logs.txt")
    pass
except:
    pass

# Function to get lifecycle logs (LC)


def getJSONResponse(next_url):
    response = requests.get('https://%s%s'%(idrac_ip,next_url), verify=False, auth=(idrac_username, idrac_password))
    data = response.json()

    return data


def get_LC_logs():

    f = open("lc_logs.txt", "w+")
    d = datetime.now()
    current_date_time = "- Data collection timestamp: %s-%s-%s  %s:%s:%s\n" % (
        d.month, d.day, d.year, d.hour, d.minute, d.second)
    f.writelines(current_date_time)
    # response = requests.get('https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Logs/Lclog' %
    #                         idrac_ip, verify=False, auth=(idrac_username, idrac_password))
    
    data = getJSONResponse('/redfish/v1/Managers/iDRAC.Embedded.1/Logs/Lclog')
    
    try:

        while(data[u'Members@odata.nextLink'] != None):
        
            time.sleep(2)
            print(data[u'Members@odata.nextLink'])

            for i in data[u'Members']:
                
                print("%s : %s"%('Id',i[u'Id']))

                data_dict = {

                    'Created' : i[u'Created'],
                    'Description': i[u'Description'],
                    'EntryType': i[u'EntryType'],
                    'Id': i[u'Id'],
                    'Message': i[u'Message'],
                    'MessageId': i[u'MessageId'],
                    'Name': i[u'Name'],
                    'OemRecordFormat': i[u'OemRecordFormat'],
                    'Severity': i[u'Severity'],



                }

                es.create(index='lc_log_index', doc_type='lc_document', id=str(
                    i[u'Id']), body=data_dict)



            print("#"*100)
            time.sleep(2)

            data = getJSONResponse(data[u'Members@odata.nextLink'])

    except KeyError as e:
        
        print("Error:",e)

        for i in data[u'Members']:

            data_dict = {

                'Created': i[u'Created'],
                'Description': i[u'Description'],
                'EntryType': i[u'EntryType'],
                'Id': i[u'Id'],
                'Message': i[u'Message'],
                'MessageId': i[u'MessageId'],
                'Name': i[u'Name'],
                'OemRecordFormat': i[u'OemRecordFormat'],
                'Severity': i[u'Severity'],

            }

            es.create(index='lc_log_index', doc_type='lc_document', id=str(
                    i[u'Id']), body=data_dict)


            print("%s : %s" % ('Id', i[u'Id']))
               
    f.close()


    

#Run Code


if __name__ == "__main__":
    get_LC_logs()


