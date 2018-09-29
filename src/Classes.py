"""
This file contains the classes this program use
"""
import threading

from KameneCustom.Arp import ArpObj, start_arp_poison_thread, start_sniff_thread, start_socket_thread, start_lab_thread
from KameneCustom.Interfaces import get_my_default_iface
from Functions.Services import PreRoutingService, IPForwardingService

class GlobalVars:
    def __init__(self):
        self.ethInterFace = ""
        self.victimArp: ArpObj = ArpObj()
        self.gatewayArp: ArpObj = ArpObj()
        self.middleArp: ArpObj = get_my_default_iface()
        
        self.arpPosion = False
        self.packets_PCAP = []
        self.packets_Commands = []
        
        self.Service_portForward = IPForwardingService()
        self.Service_preRouting = PreRoutingService()
        #lab
    def set_lab_thread(self):
        self.lab_thread = threading.Thread(target=start_lab_thread, args=(self, self.gatewayArp, self.victimArp))

    def get_stop_arp_posion(self):
        return not (self.arpPosion)
    def set_posion_thread(self):
        self.poison_thread = threading.Thread(target=start_arp_poison_thread, args=(self, self.gatewayArp, self.victimArp))
    def set_sniff_thread(self):
        self.sniff_thread = threading.Thread(target=start_sniff_thread, args=(self, self.gatewayArp, self.victimArp))
    def set_socket_thread(self):
        self.socket_thread = threading.Thread(target=start_socket_thread, args=(self, self.gatewayArp, self.victimArp))

