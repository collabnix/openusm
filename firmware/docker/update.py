# Python, Redfish & Docker Way of performing Firmware Update for DellEMC Server

import requests, json, sys, re, time, os,warnings
import argparse

from datetime import datetime

warnings.filterwarnings("ignore")


idrac_ip = idrac_username = idrac_password = firmware_file = install_option = ""





#Function to get certificate from server
def get_cert(ipaddress, port = 443):
    """
    Getting and building the SSL ceritificate.
    """

    import os
    import ssl
    from sys import stdout
    filename = "cer-"+ipaddress+".cer"
    if os.path.isfile(filename):
        print "SSL Certificate exists!"
        pass
    else:
        print 'Getting SSL Certificate. Waiting for response.',
        stdout.flush()
        cert = ssl.get_server_certificate((ipaddress,port))
        text_file = open(filename, "w")
        text_file.writelines(cert)
        text_file.close()
        print "Response received."

    return filename




def create_parser():
        parser = argparse.ArgumentParser(description='Welcome to Universal Systems Manager')

        parser.add_argument('--verbose',help='Turn on verbose logging',action='store_true')

        parser.add_argument('-i', '--ip',
                        help='iDRAC IP of the Host'
                        )
        parser.add_argument('-u', '--username',
                        help='iDRAC Username of the Host'
                        )
        parser.add_argument('-p', '--password',
                        help='iDRAC Password of the Host',
                                                )
        parser.add_argument('-f', '--file',
                        help='Firmware File'
                        )
        return parser




# Function to download the image payload to the iDRAC

def download_image_payload():
    print("\n- WARNING, downloading DUP payload to iDRAC\n")
    global Location
    global new_FW_version
    global dup_version
    global idrac_ip, idrac_username,idrac_password,firmware_file,install_option
    req = requests.get('https://%s/redfish/v1/UpdateService/FirmwareInventory/' % (idrac_ip), auth=(idrac_username, idrac_password), verify=False)
    statusCode = req.status_code
    data = req.json()
    #filename = file_image_name.lower()
    #ImageLocation = firmware_image_location
    #ImagePath = ImageLocation + "/" + filename
    head,filename = os.path.split(firmware_file)
    print "File Name %s"%(filename)
    ImagePath = firmware_file
    print "Image File %s"%(ImagePath)
    ETag = req.headers['ETag']
    url = 'https://%s/redfish/v1/UpdateService/FirmwareInventory' % (idrac_ip)
    files = {'file': (filename, open(ImagePath, 'rb'), 'multipart/form-data')}
    headers = {"if-match": ETag}
    response = requests.post(url, files=files, auth = (idrac_username, idrac_password), verify=False, headers=headers)
    d = response.__dict__
    s=str(d['_content'])
    if response.status_code == 201:
        print("\n- PASS: Command passed, 201 status code returned\n")
        z=re.search("\"Message\":.+?,",s).group().rstrip(",")
        z=re.sub('"',"",z)
        print("- %s" % z)
    else:
        print("\n- FAIL: Post command failed to download, error is %s" % response)
        print("\nMore details on status code error: %s " % d['_content'])
        sys.exit()
    d = response.__dict__
    z=re.search("Available.+?,",s).group()
    z = re.sub('[",]',"",z)
    new_FW_version = re.sub('Available','Installed',z)
    zz=z.find("-")
    zz=z.find("-",zz+1)
    dup_version = z[zz+1:]
    entry = "- FW file version is: %s" % dup_version; print(entry)
    Location = response.headers['Location']
    print Location

# Function to install the downloaded image payload and loop checking job status

def install_image_payload():
    global idrac_ip, idrac_username,idrac_password,firmware_file,install_option
    global job_id
    print("\n- WARNING, installing downloaded firmware payload to device\n")
    url = 'https://%s/redfish/v1/UpdateService/Actions/Oem/DellUpdateService.Install' % (idrac_ip)
    InstallOption = install_option
    payload = "{\"SoftwareIdentityURIs\":[\"" + Location + "\"],\"InstallUpon\":\""+ InstallOption +"\"}"
    headers = {'content-type': 'application/json'}
    print "PayLoad %s"%(payload)
    response = requests.post(url, data=payload, auth = (idrac_username, idrac_password), verify=False, headers=headers)
    d=str(response.__dict__)
    print d
    job_id_location = response.headers['Location']
    job_id = re.search("JID_.+",job_id_location).group()
    print("\n- PASS, %s job ID successfully created\n" % job_id)



# Function to check the new FW version installed

def check_new_FW_version():
    global idrac_ip, idrac_username,idrac_password,firmware_file,install_option
    print("\n- WARNING, checking new firmware version installed for updated device\n")
    req = requests.get('https://%s/redfish/v1/UpdateService/FirmwareInventory/%s' % (idrac_ip, new_FW_version), auth=(idrac_username, idrac_password), verify=False)
    statusCode = req.status_code
    data = req.json()
    if dup_version == data[u'Version']:
        print("\n- PASS, New installed FW version is: %s" % data[u'Version'])
    else:
        print("\n- FAIL, New installed FW incorrect, error is: %s" % data)
        sys.exit()

# Function to check the job status for host reboot needed

def check_job_status_host_reboot():
    global idrac_ip, idrac_username,idrac_password,firmware_file,install_option
    time.sleep(15)
    while True:
        req = requests.get('https://%s/redfish/v1/TaskService/Tasks/%s' % (idrac_ip, job_id), auth=(idrac_username, idrac_password), verify=False)
        statusCode = req.status_code
        data = req.json()
        message_string=data[u"Messages"]
        current_time=(datetime.now()-start_time)
        if statusCode == 202 or statusCode == 200:
            print("\n- Query job ID command passed\n")
            time.sleep(10)
        else:
            print("Query job ID command failed, error code is: %s" % statusCode)
            sys.exit()
        if "failed" in data[u"Messages"] or "completed with errors" in data[u"Messages"]:
            print("- FAIL: Job failed, current message is: %s" % data[u"Messages"])
            sys.exit()
        elif data[u"TaskState"] == "Completed":
            print("\n- Job ID = "+data[u"Id"])
            print("- Name = "+data[u"Name"])
            try:
                print("- Message = "+message_string[0][u"Message"])
            except:
                print("- Message = "+data[u"Messages"][0][u"Message"])
            print("- JobStatus = "+data[u"TaskState"])
            print("\n- %s completed in: %s" % (job_id, str(current_time)[0:7]))
            break
        elif data[u"TaskState"] == "Completed with Errors" or data[u"TaskState"] == "Failed":
            print("\n- Job ID = "+data[u"Id"])
            print("- Name = "+data[u"Name"])
            try:
                print("- Message = "+message_string[0][u"Message"])
            except:
                print("- "+data[u"Messages"][0][u"Message"])
            print("- JobStatus = "+data[u"TaskState"])
            print("\n- %s completed in: %s" % (job_id, str(current_time)[0:7]))
            sys.exit()
        else:
            print("- Job not marked completed, current status is: %s" % data[u"TaskState"])
            print("- Message: %s\n" % message_string[0][u"Message"])
            print("- Current job execution time is: %s\n" % str(current_time)[0:7])
            time.sleep(1)
            continue

def check_job_status():
    global idrac_ip, idrac_username,idrac_password,firmware_file,install_option
    # Loop get commnad to check the job status of completed, completed with errors or failed

    start_time=datetime.now()
    while True:
        req = requests.get('https://%s/redfish/v1/TaskService/Tasks/%s' % (idrac_ip, job_id), auth=(idrac_username, idrac_password), verify=False)
        statusCode = req.status_code
        data = req.json()
        message_string=data[u"Messages"]
        current_time=(datetime.now()-start_time)
        if statusCode == 202 or statusCode == 200:
            print("\n- Query job ID command passed\n")
            time.sleep(10)
        else:
            print("Query job ID command failed, error code is: %s" % statusCode)
            sys.exit()
        if "failed" in data[u"Messages"] or "completed with errors" in data[u"Messages"]:
            print("- FAIL: Job failed, current message is: %s" % data[u"Messages"])
            sys.exit()
        elif data[u"TaskState"] == "Pending":
            print("\n- Job ID = "+data[u"Id"])
            print("- Name = "+data[u"Name"])
            try:
                print("- Message = "+message_string[0][u"Message"])
            except:
                print("- Message = "+data[u"Messages"][0][u"Message"])
            print("- JobStatus = "+data[u"TaskState"])
            print("\n- %s scheduled in: %s" % (job_id, str(current_time)[0:7]))
            print("\n- WARNING, Host manual reboot is now needed to complete the process of applying the firmware image.\n")
            break
        elif data[u"TaskState"] == "Completed":
            print("\n- WARNING, device selected is immediate update, incorrect install option passed in.")
            print("- %s still marked completed and firmware updated" % (job_id))
            break
        elif data[u"TaskState"] == "Completed with Errors" or data[u"TaskState"] == "Failed":
            print("\n- Job ID = "+data[u"Id"])
            print("- Name = "+data[u"Name"])
            try:
                print("- Message = "+message_string[0][u"Message"])
            except:
                print("- "+data[u"Messages"][0][u"Message"])
            print("- JobStatus = "+data[u"TaskState"])
            print("\n- %s completed in: %s" % (job_id, str(current_time)[0:7]))
            sys.exit()
        else:
            print("- Job not marked completed, current status is: %s" % data[u"TaskState"])
            print("- Message: %s\n" % message_string[0][u"Message"])
            print("- Current job execution time is: %s\n" % str(current_time)[0:7])
            time.sleep(1)
            continue



def main():
        global idrac_ip, idrac_username,idrac_password,firmware_file,install_option
        # Code to validate all correct parameters are passed in
        try:
                # parser = create_parser()
                # args = parser.parse_args()
                #
                # idrac_ip = args.ip
                # idrac_username = args.username
                # idrac_password = args.password
                # firmware_file = args.file
                # idrac_ip = "100.98.26.37";
                idrac_ip = os.environ['IDRAC_IP']

                idrac_username = os.environ['USERNAME']

                idrac_password = os.environ['PASSWORD']

                # file_name = "R730_myxmlSCP.xml";
                firmware_file = os.environ['FIRMWARE_FILE']

                firmware_file = os.path.abspath(firmware_file)


        except Exception as e:
                print("\n- FAIL, you must pass in script name along with iDRAC IP / iDRAC username / iDRAC password / Image Path / Filename / Install Option. Example: \" script_name.py 192.168.0.120 root calvin c:\Python26 bios.exe NowAndReboot\"")
                print e.message
                sys.exit()

        print idrac_ip,idrac_password,idrac_username,firmware_file
        start_time=datetime.now()
        Install_Option = "nowandreboot"

        # Code to convert install option to correct string due to case sensitivity in iDRAC.
        if Install_Option == "now":
                install_option = "Now"
        elif Install_Option == "nowandreboot":
                install_option = "NowAndReboot"
        elif Install_Option == "nextreboot":
                install_option = "NextReboot"
        else:
                install_option = Install_Option

        download_image_payload()
        install_image_payload()
        if install_option == "NowAndReboot" or install_option == "Now":
                check_job_status_host_reboot()
                check_new_FW_version()
        else:
                check_job_status()



if __name__ == "__main__":
        main()


'''
# Run code here

download_image_payload()
install_image_payload()
if install_option == "NowAndReboot" or install_option == "Now":
    check_job_status_host_reboot()
    check_new_FW_version()
else:
    check_job_status()
'''
