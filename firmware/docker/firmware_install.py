# Python, Redfish & Docker Way of performing Firmware Update for DellEMC Server
# Test
import requests, json, sys, re, time, os,warnings
import argparse

from datetime import datetime

warnings.filterwarnings("ignore")


idrac_ip = idrac_username = idrac_password = firmware_file = install_option = ""


def create_parser():
        parser = argparse.ArgumentParser(description='Welcome to Universal Systems Manager')

        parser.add_argument('--verbose',
                            help='Turn on verbose logging',
                            action='store_true')

        parser.add_argument('-i', '--idrac',
                            help='iDRAC IP of the Single Host'
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

        parser.add_argument('-s', '--ips',
                            help='IP files to be updated'
                            )
        return parser

def main():
        global idrac_ip, idrac_username,idrac_password,firmware_file,install_option
        # Code to validate all correct parameters are passed in
        try:
                parser = create_parser()
                args = parser.parse_args()

                idrac_ip = args.idrac
                idrac_username = args.username
                idrac_password = args.password
                firmware_file = args.file

                firmware_file = os.path.abspath(firmware_file)

                print idrac_ip, idrac_password, idrac_username, firmware_file

                os.system("docker build -t ajeetraina/openusm . ")

                if (args.ips):

                    ip_file = args.ips
                    ips_file = open(ip_file)
                    ips = ips_file.readlines()

                    for ip in ips:
                        print ("Iteration %s" % ip)

                        ip = ip.strip()
                        command = "docker run -v `pwd`:`pwd` --log-driver=syslog --log-opt syslog-address=tcp://100.98.26.181:5000 --log-opt syslog-facility=daemon -itd --name=%s_server -e IDRAC_IP=%s  -e USERNAME=%s -e PASSWORD=%s -e FIRMWARE_FILE=%s ajeetraina/openusm python update.py &" % (
                        ip, ip, idrac_username,idrac_password,firmware_file)
                        print command
                        os.system(command)

                if (args.idrac):
                    print "Entering the Execution"
                    test = os.system("docker run -v `pwd`:`pwd` -itd --name=%s_server -e IDRAC_IP=%s -e USERNAME=%s -e PASSWORD=%s -e FIRMWARE_FILE=%s ajeetraina/openusm python update.py &" % (idrac_ip, idrac_ip, idrac_username,idrac_password,firmware_file))
                    print test

        except Exception as e:
                print("\n- FAIL, you must pass in script name along with iDRAC IP / iDRAC username / iDRAC password / Image Path / Filename / Install Option. Example: \" script_name.py 192.168.0.120 root calvin c:\Python26 bios.exe NowAndReboot\"")
                print e.message
                sys.exit()




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
