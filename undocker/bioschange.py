
import os, requests, json, sys, re, time
from datetime import datetime

import argparse

requests.packages.urllib3.disable_warnings()


def _create_parser():

        parser = argparse.ArgumentParser(description='Welcome to Universal Systems Manager'
                                                 'Bios Token Change')

        parser.add_argument('--verbose',
                        help='Turn on verbose logging',
                        action='store_true')

        parser.add_argument('-n', '--nfs',
                        help='NFS server IP address',
                        default=None)
        parser.add_argument('-s', '--share',
                        help='NFS Share folder'
                        )
        parser.add_argument('-c', '--config',
                       help='XML File to be imported'
                      )

        parser.add_argument('-f', '--file',
                        help='IP files to be updated'
                        )

        return parser


def import_scp(idrac_ip,share_ip,share_name,file_name):
        url = 'https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ImportSystemConfiguration' % idrac_ip
        payload = {"ExportFormat":"XML","ShareParameters":{"Target":"ALL","IPAddress":share_ip, "ShareName":share_name, "ShareType":"NFS","FileName":file_name}}
        print url
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,auth=('root','calvin'))
        if response.status_code != 202:
                print "\n##### Command Failed, status code not 202\n, code is: %s" % response.status_code
                #sys.exit()
                return
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
                        #sys.exit()
                        return
                if "failed" in data[u"Messages"] or "completed with errors" in data[u"Messages"]:
                        print "Job failed, current message is: %s" % data[u"Messages"]
                        #sys.exit()
                        return
                elif data[u"TaskState"] == "Completed":
                        print "\nJob ID = "+data[u"Id"]
                        print "Name = "+data[u"Name"]
                        print "Message = "+message_string[0][u"Message"]
                        print "JobStatus = "+data[u"TaskState"]
                        print "\n%s completed in: %s" % (job_id, str(current_time)[0:7])
                        #sys.exit()
                        return
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


def main():

        parser = _create_parser()
        args = parser.parse_args()

        # share_ip = "100.98.26.42";
        share_ip = args.nfs
        # share_ip = "100.98.24.144";

        # share_name = "/var/nfsshare";
        share_name = args.share
        # share_name = "/var/nfsshare";

        # file_name = "R730_myxmlSCP.xml";
        config_file = args.config
        # file_name = "biosconfig.xml";

        file_name = args.file


        ########
        print("NFS_SERVER %s -- NFS_SERVER_SHARE %s CONFIG_FILE %s "%(share_ip, share_name, file_name))

        # reading the file

        f = open(file_name)

        server_ips = f.readlines()

        for server in server_ips:
                print("Server ---- ",server.strip(), share_ip.strip(), share_name, file_name)
                import_scp(server.strip(), share_ip.strip(), share_name, config_file)



if __name__ == '__main__':
        main()
