from scapy.all import *

class myTunnel(Packet):
	name = "myTunnel"
	fields_desc = [ShortField("proto_id",5),ShortField("dst_id",0)]

bind_layers(Ether,myTunnel,type = 0x1212)
packet = Ether(src = "00:04:00:00:00:00",type = 0x1212)/myTunnel(proto_id=0x0800,dst_id = 2)/IP(src="10.0.0.10",dst = "10.0.1.10")
#packet = Ether(src = "00:04:00:00:00:00")/IP(src="10.0.0.10",dst = "10.0.1.10")
#packet = Ether(src = "00:04:00:00:00:00",type = 0x1212)/myTunnel(proto_id=0x800,dst_id = 2)/IP(src="10.0.0.10",dst = "10.0.1.10")
sendp(packet)

