import json
import sys
import re
import time
import os
import commands
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

    parser.add_argument('-ei', '--elastic_ip',
                        help='Ip Address of the Elastic'
                        )

    parser.add_argument('-eu', '--elastic_username',
                        help='Username of the Elastic'
                        )

    parser.add_argument('-ep', '--elastic_password',
                        help='Password of the Elastic'
                        )

    parser.add_argument('-s', '--subnet', help='Subnet: Provide Network Id with Subnet Mask(in Integer form)' )

    return parser


def main():
    parser = _create_parser()
    args = parser.parse_args()


    elastic_ip = args.elastic_ip
    elastic_username = args.elastic_username
    elastic_password = args.elastic_password
    subnet_mask=args.subnet
#    print(subnet_mask)

    print("Scanning Subnet to Find Hosts")
    cmd="nmap -sn %s | grep \"Nmap scan\" | awk '{print $NF}'" % subnet_mask
#    print(cmd)
    ips=commands.getoutput(cmd)
#    print(ips)
    ips_list=ips.split("\n")
    for i in range(0, len(ips_list), 1):
        ips_list[i]=ips_list[i].lstrip("(").rstrip(")")

    os.system("docker build -t ajeetraina/openusm_analytics . ")

    for ip in ips_list:

            command = "docker run --rm -itd --name=%s_server -e IDRAC_IP=%s -e IDRAC_USERNAME=%s -e IDRAC_PASSWORD=%s -e ELASTIC_IP=%s -e ELASTIC_USERNAME=%s -e ELASTIC_PASSWORD=%s ajeetraina/openusm_analytics python docker_lc_exporter.py &" % (ip, ip, 'root', 'calvin', elastic_ip,elastic_username,elastic_password)
            os.system(command)

if __name__ == '__main__':
    main()
