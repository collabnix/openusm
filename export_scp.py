import os, requests, json,re

requests.packages.urllib3.disable_warnings()

#idrac_ip = "100.98.26.37";
idrac_ip= os.environ['IDRAC_IP']

#share_ip = "100.98.26.42";
share_ip= os.environ['NFS_SERVER']

#share_name = "/var/nfsshare";
share_name = os.environ['NFS_SERVER_SHARE']

#file_name = "R730_myxmlSCP.xml";
file_name = os.environ['CONFIG_FILE']




url = 'https://'+ idrac_ip +'/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ExportSystemConfiguration'

payload = {"ExportFormat":"XML","ShareParameters":{"Target":"ALL","IPAddress": share_ip,"ShareName":share_name,"ShareType":"NFS","FileName":file_name}}

headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,

auth=('root','calvin'))

print '- Response status code is: %s' % response.status_code

response_output=response.__dict__

print response_output

#job details
job_id=response_output["headers"]["Location"]
job_id=re.search("JID_.+",job_id).group()
print "- Job ID is: %s" % job_id
