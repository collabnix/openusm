import json
import sys
import re
import time
import os
import warnings
from datetime import datetime
import argparse

warnings.filterwarnings("ignore")
def _create_parser():
    parser = argparse.ArgumentParser(description='Welcome to Universal Systems Manager'
                                                 'Bios Token Change')
    parser.add_argument('--verbose',
                        help='Turn on verbose logging',
                        action='store_true')

    parser.add_argument('-i', '--idrac',
                        help='iDRAC IP of the Host'
                        )

    parser.add_argument('-f', '--ips',
                        help='IP files to be updated'
                        )

    parser.add_argument('-ei', '--elastic_ip',
                        help='Ip Address of the Elastic'
                        )

    parser.add_argument('-eu', '--elastic_username',
                        help='Username of the Elastic'
                        )

    parser.add_argument('-ep', '--elastic_password',
                        help='Password of the Elastic'
                        )

    return parser


def main():
    parser = _create_parser()
    args = parser.parse_args()

    idrac = args.idrac
    elastic_ip = args.elastic_ip
    elastic_username = args.elastic_username
    elastic_password = args.elastic_password

    os.system("docker build -t ajeetraina/openusm-analytics . ")
    if (args.ips):

        ip_file = args.ips
        ips_file = open(ip_file)
        ips = ips_file.readlines()

        for ip in ips:
            print ("Iteration %s" % ip)

        ip = ip.strip()
        command = "docker run --rm --log-driver=syslog --log-opt syslog-address=tcp://0.0.0.0:5000 --log-opt syslog-facility=daemon -itd --name=%s_server -e IDRAC_IP=%s -e IDRAC_USERNAME=%s -e IDRAC_PASSWORD=%s -e ELASTIC_IP=%s -e ELASTIC_USERNAME=%s -e ELASTIC_PASSWORD=%s ajeetraina/openusm-analytics python docker_lc_exporter.py &" % (
        ip, ip, 'root', 'calvin', elastic_ip,elastic_username,elastic_password)
        print command
        os.system(command)

    if (args.idrac):
        print ("Iteration %s" % args.idrac)

        command = "docker run --rm --log-driver=syslog --log-opt syslog-address=tcp://0.0.0.0:5000 --log-opt syslog-facility=daemon -itd --name=%s_server -e IDRAC_IP=%s -e IDRAC_USERNAME=%s -e IDRAC_PASSWORD=%s -e ELASTIC_IP=%s -e ELASTIC_USERNAME=%s -e ELASTIC_PASSWORD=%s ajeetraina/openusm-analytics python docker_lc_exporter.py &" % (
        idrac, idrac, 'root', 'calvin', elastic_ip,elastic_username,elastic_password)

        os.system(command)

if __name__ == '__main__':
    main()

