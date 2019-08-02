'''
Created on Jun 9, 2017

@author: Avinash_Bendigeri
'''


import json


import json
from pprint import pprint

print "Hello world"

with open('bios.json') as data_file:    
    data = json.load(data_file)

print data

pprint(data)
