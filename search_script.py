from __future__ import division
import requests
import json
import sys
import os
from elasticsearch import Elasticsearch
from elasticsearch import exceptions

try:
#    idrac_ip = os.environ['IDRAC_IP']
#    idrac_username = os.environ['IDRAC_USERNAME']
#    idrac_password = os.environ['IDRAC_PASSWORD']

#    elastic_ip = os.environ['ELASTIC_IP']
#    elastic_username = os.environ['ELASTIC_USERNAME']
#    elastic_password = os.environ['ELASTIC_PASSWORD']
    idrac_ip="100.98.26.49"
    idrac_username="root"
    idrac_password="calvin"
    elastic_ip="100.98.26.172"
    elastic_username="elastic"
    elastic_password="changeme"
    es = Elasticsearch([elastic_ip],
                       http_auth=(elastic_username, elastic_password),
                       scheme="http",
                       port=9200,
                       )
except Exception as e:
    print("- FAIL: You must pass in script name along with iDRAC IP / iDRAC username / iDRAC password")
    sys.exit(0)

def retrieve_logs():
    index_name="lc"+idrac_ip
    res=es.search(index=index_name, body={
          "query":{
              "range": {
                 "timestamp": {
                      "gte" : "now-5m",
                      "lt" : "now"
                  }
               }
           }
        }
    )
   # print(data)
    codes = {}
    code_types={}
    for i in res['hits']['hits']:
        #print(i)
        #print("\n")
        for key,value in i['_source'].items():
            if key=='MessageID':
               code=value
               code_type=value[0:3]
               #print(code_type)
               if code in codes:
                  codes[code]=codes[code]+1
               else:
                  codes.update({code: 1})
               if code_type in code_types:
                  code_types[code_type]=code_types[code_type]+1
               else:
                  code_types.update({code_type: 1})

    total_errors=sum(codes.values())
#    print total_errors
    error_percentage={}

    print "\nFor Server: ",idrac_ip
#    print "__________________________ \n\n\n"
    print("\n\n\n")
    print "Error Codes     Occurrence       Percentage "
    print "____________________________________________ \n"
    for key,value in codes.items():
        error_percentage[key]= (value/total_errors)*100
    	print key,"        ",value,"               ",error_percentage[key],"%"

    print "\n"
    print "Error Types     Occurrence "
    print "__________________________ \n"

    for key,value in code_types.items():
        print key,"            ",value

#    print(codes)
#    print(code_types)


#    print (total_errors)
#    print error_percentage



retrieve_logs()
