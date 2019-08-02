import os
import argparse


def _create_parser():
    parser = argparse.ArgumentParser(description='Welcome to Universal Systems Manager'
                                                 'Bios Token Change')
    parser.add_argument('--verbose',
                        help='Turn on verbose logging',
                        action='store_true')

    parser.add_argument('-i', '--idrac',
                        help='iDRAC IP of the Host'
                        )

    parser.add_argument('-n', '--nfs',
                        help='NFS server IP address',
                        default=None)

    parser.add_argument('-s', '--share',
                        help='NFS Share folder'
                        )

    parser.add_argument('-c', '--config',
                        help='XML File to be imported'
                        )

    parser.add_argument('-f', '--ips',
                        help='IP files to be updated'
                        )

    return parser


def main():
    parser = _create_parser()
    args = parser.parse_args()

    nfs_server = args.nfs
    idrac = args.idrac
    nfs_share = args.share
    config = args.config

    os.system("docker build -t ajeetraina/usm_redfish . ")

    if(args.ips):

        ip_file = args.ips
        ips_file = open(ip_file)
        ips =  ips_file.readlines()

        for ip in ips:
	    print ("Iteration %s"%ip)

	    ip = ip.strip()	
	    command = "docker run --rm --log-driver=syslog --log-opt syslog-address=tcp://0.0.0.0:5000 --log-opt syslog-facility=daemon -itd --name=%s_server -e IDRAC_IP=%s -e NFS_SERVER=%s -e NFS_SERVER_SHARE=%s -e CONFIG_FILE=%s ajeetraina/usm_redfish python import_scp.py &"%(ip,ip,nfs_server,nfs_share,config)
	    print command
	    os.system(command)

    if (args.idrac):
        os.system(
                "docker run --rm --log-driver=syslog --log-opt syslog-address=tcp://0.0.0.0:5000 --log-opt syslog-facility=daemon -itd --name=%s_server -e IDRAC_IP=%s -e NFS_SERVER=%s -e NFS_SERVER_SHARE=%s -e CONFIG_FILE=%s ajeetraina/usm_redfish  python import_scp.py &" % (
                idrac,idrac, nfs_server, nfs_share, config))

if __name__ == '__main__':
    main()
