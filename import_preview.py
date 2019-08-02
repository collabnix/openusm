#
# Python iDRAC REST API script to preview import of system configuration profile
#
import requests, json, re

requests.packages.urllib3.disable_warnings()

idrac_ip = "100.98.26.37";

share_ip = "100.98.26.42";

share_name = "/var/nfsshare";

file_name = "new.xml";



url = 'https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ImportSystemConfigurationPreview'% idrac_ip
payload = {"ExportFormat":"XML","ShareParameters":{"Target":"ALL","IPAddress":share_ip,"ShareName":share_name,"ShareType":"NFS","FileName":"R730_SCP.xml","UserName":"user","Password":"password"}}
headers = {'content-type': 'application/json'}
response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False, auth=('root','calvin'))
print '- Response status code is: %s' % response.status_code
response_output=response.__dict__
job_id=response_output["headers"]["Location"]
job_id=re.search("JID_.+",job_id).group()
print "- Job ID is: %s" % job_id
