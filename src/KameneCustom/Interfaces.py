'''
This file contains the kamene interface functions this program use
'''
from kamene.config import conf
from kamene.arch import get_if_hwaddr
from kamene.sendrecv import sr
from kamene.layers.l2 import ARP

from KameneCustom.Arp import ArpObj

def get_my_default_iface():
    myArp = ArpObj()
    myArp.MACAddress = get_if_hwaddr(conf.iface)
    myArp.IPAddress = [x[4] for x in conf.route.routes if x[2] != '0.0.0.0'][0]
    return myArp
    
def get_mac(ip_address):
    #ARP request is constructed. sr function is used to send/ receive a layer 3 packet
    #Alternative Method using Layer 2: resp, unans =  srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ip_address))
    resp = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
    for s,r in resp:
        return r[ARP].hwsrc
    return None