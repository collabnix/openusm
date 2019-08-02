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

    parser.add_argument('-d', '--counter',
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

    os.system("docker build -t ajeetraina/counter . ")

    if(args.counter):
	counter = int(args.counter)
        for ip in range(0,counter+1):
	    print ("Iteration %s"%ip)
	   	
	    command = "docker run -d --name=%s_server ajeetraina/counter python ping.py &"%(ip)
	    print command
	    os.system(command)

    if (args.idrac):
        os.system(
                "docker run -d --name=%s_server ajeetraina/counter  python ping.py &"%(idrac))

if __name__ == '__main__':
    main()
