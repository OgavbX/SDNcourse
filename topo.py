from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI

from p4_mininet import P4Switch, P4Host

import argparse
from time import sleep

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", required=True)
parser.add_argument('--thrift-port', help='Thrift server port for table updates',
                    type=int, action="store", default=9090)
parser.add_argument('--num-hosts', help='Number of hosts to connect to switch',
                    type=int, action="store", default=3)
parser.add_argument('--mode', choices=['l2', 'l3'], type=str, default='l3')
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=True)
parser.add_argument('--pcap-dump', help='Dump packets on interfaces to pcap files',
                    type=str, action="store", required=False, default=False)

args = parser.parse_args()




class myTopo(Topo):
    "2 hosts connected by 4 switches."
    def __init__(self, sw_path, json_path, thrift_port, pcap_dump, n, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        #add switches
        s1 = self.addSwitch('s1',
                                sw_path = sw_path,
                                json_path = json_path,
                                thrift_port = thrift_port,
                                pcap_dump = pcap_dump)

	s2 = self.addSwitch('s2',
                                sw_path = sw_path,
                                json_path = json_path,
                                thrift_port = thrift_port+1,
                                pcap_dump = pcap_dump)

	s3 = self.addSwitch('s3',
                                sw_path = sw_path,
                                json_path = json_path,
                                thrift_port = thrift_port+2,
                                pcap_dump = pcap_dump)

	#s4 = self.addSwitch('s4',
        #                        sw_path = sw_path,
         #                       json_path = json_path,
         #                      thrift_port = thrift_port+3,
        #                       pcap_dump = pcap_dump)

	#add hosts
        #for h in xrange(n):
           # host = self.addHost('h%d' % (h + 1),
           #                     ip = "10.0.%d.10/24" % h,
           #                     mac = '00:04:00:00:00:%02x' %h)
	h1 = self.addHost('h1',
                                ip = "10.0.0.10/24",
                                mac = '00:04:00:00:00:01')
	h2 = self.addHost('h2',
                                ip = "10.0.1.10/24",
                                mac = '00:04:00:00:00:02')
	h3 = self.addHost('h3',
                                ip = "10.0.2.10/24",
                                mac = '00:04:00:00:00:03')

	#add links
	self.addLink(h1,s1)
	self.addLink(h2,s2)
	self.addLink(h3,s3)
	self.addLink(s1,s2)
	self.addLink(s2,s3)
	self.addLink(s1,s3)
	#self.addLink(s1,s3)
	#self.addLink(s3,s4)
	#self.addLink(s4,h2)


def main():
    num_hosts = args.num_hosts
    mode = args.mode

    topo = myTopo(args.behavioral_exe,
                            args.json,
                            args.thrift_port,
                            args.pcap_dump,
                            num_hosts)
    net = Mininet(topo = topo,
                  host = P4Host,
                  switch = P4Switch,
                  controller = None)
    net.start()


    sw_mac = ["00:aa:bb:00:00:%02x" % n for n in xrange(num_hosts)]
    #sw_mac = ["00:aa:bb:00:00:01","00:aa:bb:00:00:02" ]
    sw_addr = ["10.0.%d.1" % n for n in xrange(num_hosts)]
    #sw_addr = ["10.0.0.1","10.0.1.1"]

    for n in xrange(num_hosts):
    #for n in range(0,2):
        h = net.get('h%d' % (n + 1))
        if mode == "l2":
            h.setDefaultRoute("dev eth0")
        else:
            h.setARP(sw_addr[n], sw_mac[n])
            h.setDefaultRoute("dev eth0 via %s" % sw_addr[n])

    for n in xrange(num_hosts):
    #for n in range(0,2):
        h = net.get('h%d' % (n + 1))
        h.describe()

    sleep(1)

    print "Ready !"

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
