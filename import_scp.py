import os, requests, json, sys, re, time
from datetime import datetime

requests.packages.urllib3.disable_warnings()



#idrac_ip = "100.98.26.37";
idrac_ip= os.environ['IDRAC_IP']

#share_ip = "100.98.26.42";
share_ip= os.environ['NFS_SERVER']

#share_name = "/var/nfsshare";
share_name = os.environ['NFS_SERVER_SHARE']

#file_name = "R730_myxmlSCP.xml";
file_name = os.environ['CONFIG_FILE']


########
print("IDRAC IP %s -- NFS_SERVER %s -- NFS_SERVER_SHARE %s CONFIG_FILE %s "%(idrac_ip,share_ip,share_name,file_name))



url = 'https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ImportSystemConfiguration' % idrac_ip
payload = {"ExportFormat":"XML","ShareParameters":{"Target":"ALL","IPAddress":share_ip, "ShareName":share_name, "ShareType":"NFS","FileName":file_name}}
print url
headers = {'content-type': 'application/json'}
response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,auth=('root','calvin'))
if response.status_code != 202:
	print "\n##### Command Failed, status code not 202\n, code is: %s" % response.status_code
	sys.exit()
else:
	print "\n- Job ID successfully created"
	response_output=response.__dict__
	job_id=response_output["headers"]["Location"]
	job_id=re.search("JID_.+",job_id).group()
	start_time=datetime.now()
while True:
	req = requests.get('https://%s/redfish/v1/TaskService/Tasks/%s' % (idrac_ip, job_id),auth=("root", "calvin"), verify=False)
	statusCode = req.status_code
	data = req.json()
	message_string=data[u"Messages"]
	current_time=(datetime.now()-start_time)

	if statusCode == 202 or statusCode == 200:
		print "\n- Query job ID command passed"
	else:
		print "Query job ID command failed, error code is: %s" % statusCode
		sys.exit()
	if "failed" in data[u"Messages"] or "completed with errors" in data[u"Messages"]:
		print "Job failed, current message is: %s" % data[u"Messages"]
		sys.exit()
	elif data[u"TaskState"] == "Completed":
		print "\nJob ID = "+data[u"Id"]
		print "Name = "+data[u"Name"]
		print "Message = "+message_string[0][u"Message"]
		print "JobStatus = "+data[u"TaskState"]
		print "\n%s completed in: %s" % (job_id, str(current_time)[0:7])
		sys.exit()
	else:
		print "- Job not marked completed, current status is: %s" % data[u"TaskState"]
		print "- Message: %s\n" % message_string[0][u"Message"]
		time.sleep(1)
		continue
data = req.json()
print "Job ID = "+data[u"Id"]
print "Name = "+data[u"Name"]
print "Message = "+data[u"Messages"]
print "JobStatus = "+data[u"TaskState"]

url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset'%idrac_ip
payload = {'ResetType': 'GracefulRestart'}
headers = {'content-type': 'application/json'}
response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,auth=('root','calvin'))

print response
