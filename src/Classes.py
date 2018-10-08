from HMGeneric.internetProtocol import ArpObj
from HMGeneric.ethernet import get_my_interface
from HMGeneric.menu import MenuRoot

from HMKamene.arp import ArpThread
from Services import IPForwardingService, PreRoutingService
class GlobalVars:
    def __init__(self):
        self.myInterface = get_my_interface()
        self.victimArp: ArpObj = ArpObj()
        self.gatewayArp: ArpObj = ArpObj()
        self.middleArp: ArpObj = ArpObj()
        self.middleArp.MACAddress = self.myInterface['mac']
        self.middleArp.IPAddress = self.myInterface['ip']
                
        self.Service_portForward = IPForwardingService()
        self.Service_preRouting = PreRoutingService()

        self.menu = MenuRoot(self)

        self.arpPosion = ArpThread(self.gatewayArp, self.victimArp)