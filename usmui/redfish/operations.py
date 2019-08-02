'''
Created on Jun 15, 2017

@author: Avinash_Bendigeri
'''
import requests
import json
import datetime
import sys
import re
from pprint import pprint

def powerOn(server):
    ip = server.ip
    username = server.username
    password = server.password
    
    
    url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset'%ip
    payload = {'ResetType': 'On'}
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,auth=(username,password))
    print response
    
def resetServer(server):
    ip = server.ip
    username = server.username
    password = server.password
    
    
    url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset'%ip
    payload = {'ResetType': 'GracefulRestart'}
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,auth=(username,password))
    print "myresponse", response    
    
def systemDetails(server):
    
    outputdata= {}
    
    ip = server.ip
    username = server.username
    password = server.password
    
    url = 'https://%s/redfish/v1/Systems/System.Embedded.1'%ip
    headers = {'content-type': 'application/json'}
    response = requests.get(url,headers=headers, verify=False,auth=(username,password))
    
    data = response.json()
    
    outputdata['BiosVersion'] = data['BiosVersion']
    outputdata['Model'] = data['Model']
    outputdata['SerialNumber'] = data['SerialNumber']
    outputdata['Memory'] = data['MemorySummary']['TotalSystemMemoryGiB']
    
    
    
    print outputdata
    
    
    return outputdata

def importSCPServer(server):
    
    ip = server.ip
    username = server.username
    password = server.password
    
    

    share_ip = "10.94.214.181";

    share_name = "/var/nfsshare";

    file_name = "new.xml";
    
    url = 'https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ImportSystemConfiguration' % ip
    
    print url
    
    payload = {"ExportFormat":"XML","ShareParameters":{"Target":"ALL","IPAddress":share_ip, "ShareName":share_name, "ShareType":"NFS","FileName":file_name}}
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,auth=(username,password))
    print "Response ",dir(response)
    if response.status_code != 202:
        print "\n##### Command Failed, status code not 202\n, code is: %s" % response.status_code
        
        print response.json()
        
        return "Error"
    else:
        print "\n- Job ID successfully created"
        response_output=response.__dict__
        job_id=response_output["headers"]["Location"]
        job_id=re.search("JID_.+",job_id).group()
        start_time=datetime.datetime.now()
        
        
        url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset'%ip
        payload = {'ResetType': 'GracefulRestart'}
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,auth=(username,password))

    return "Success"

def getBiosTokens(server):
    ip = server.ip
    username = server.username
    password = server.password
    
    url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Bios'%ip
    headers = {'content-type': 'application/json'}
    response = requests.get(url,headers=headers, verify=False,auth=(username,password))
     
    biosdata = response.json()
    biosdata =  biosdata['Attributes']
    
    return biosdata

def generateXML(settings):
    
 
    from xml.dom import minidom
    xmldoc = minidom.parse('xml_profiles/template.xml')
    itemlist = xmldoc.getElementsByTagName('Attribute')
    print(len(itemlist))
    # print(itemlist[0].attributes['Name'].value)
    for s in itemlist:
        if s.attributes['Name'].value in ['ProcVirtualization','ControlledTurbo','LogicalProc']:
#             print s.attributes['Name'].value
            
    #         s.set_value(test[s.attributes['Name'].value])
            s.firstChild.data = settings[s.attributes['Name'].value]
            
            
            
    
    file_handle = open('xml_profiles/my.xml',"wb")
    xmldoc.writexml(file_handle)
    file_handle.close()