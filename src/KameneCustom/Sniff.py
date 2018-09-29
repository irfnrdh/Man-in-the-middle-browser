'''
This file contains the kamene sniffing functions this program use
'''

from kamene.sendrecv import sniff
from kamene.utils import wrpcap
from kamene.layers.dns import IP

from KameneCustom.Arp import ArpObj
from KameneCustom.Packets import genereate_packet, generate_lab_packet

def start_sniff_thread(globalVars, gatewayArp: ArpObj, victimArp: ArpObj):
    def packet_get(packet):
        try:
            if(packet.src == victimArp.MACAddress or packet[IP].dst == victimArp.IPAddress):
                genereate_packet(packet, globalVars)
        except:
            print("")
    sniff(prn=packet_get, store=0, stop_callback=globalVars.get_stop_arp_posion)
    '''filter="src host "+ victimArp.IPAddress + " or src host " + gatewayArp.IPAddress , '''
    for pkt in globalVars.packets_PCAP:
        wrpcap("test.pcap", pkt, append=True)

def start_lab_thread(globalVars, gatewayArp: ArpObj, victimArp: ArpObj):
    def packet_get(packet):
        try:
            if(packet[IP].dst == victimArp.IPAddress or packet[IP].src == victimArp.IPAddress):
                generate_lab_packet(packet, globalVars)
        except:
            s=1

    sniff(prn = packet_get, store=0, stop_callback=globalVars.get_stop_arp_posion)
    for pkt in globalVars.packets_PCAP:
        wrpcap("test.pcap", pkt, append=True)

    with open('listfile.txt', 'w') as filehandle:  
        filehandle.writelines("%s\n" % pkt for pkt in globalVars.packets_Commands)
    return 1