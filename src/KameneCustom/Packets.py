'''
This file contains the kamene packet generating functions this program use
'''

from kamene.layers.l2 import Ether, Packet, ARP
from kamene.layers.dns import DNS, IP, TCP, UDP, DNSQR, DNSRR, Raw
from kamene.layers.netbios import NBNSQueryRequest
from kamene.layers.ipsec import IPv6
from kamene.packet import ls
from kamene.sendrecv import sr1, send

def generate_lab_packet(oldPacket: Packet, globalVars):
    #print(str(len(oldPacket[TCP].load)))
    command_text = []
    command_text.append("#-------------"+str(len(globalVars.packets_Commands)/4+1)+"--------------")
    text_second_line = ""
    try:
        if(oldPacket[Ether].src == globalVars.victimArp.MACAddress):
            text_second_line = "<Victim> : "
        elif(oldPacket[Ether].src == globalVars.gatewayArp.MACAddress):
            text_second_line = "<Gate> : "
        elif(oldPacket[Ether].src == globalVars.middleArp.MACAddress):
            text_second_line = "<Middle> : "
        else:
            print("doesnt need to happen")
    except:
        #doesn't have ether layer
        print("expect")
    if(IPv6 in oldPacket):
        command_text.append(text_second_line +"IPv6")
    elif(DNS in oldPacket):
        command_text.append(text_second_line +"DNS")
        #oldPacket.show()
    elif(TCP in oldPacket):
        command_text.append(text_second_line +"TCP")
        #oldPacket.show()
    elif(ARP in oldPacket):
        command_text.append(text_second_line +"ARP")
        #oldPacket.show()
    elif(UDP in oldPacket):
        command_text.append(text_second_line +"UDP")
        #oldPacket.show()
    else:
        command_text.append(text_second_line +"<New>")
        #oldPacket.show()

    command_text.append(oldPacket.command())
    command_text.append('\n\n\n\n')
    globalVars.packets_Commands.extend(command_text)
    globalVars.packets_PCAP.append(oldPacket)

def genereate_packet(oldPacket: Packet, globalVars):

    def generate_dns():
        if(oldPacket[Ether].src == globalVars.victimArp.MACAddress):
            DNSRequest =\
            IP(src=oldPacket[IP].src, dst=oldPacket[IP].dst)\
            /UDP(sport=oldPacket[UDP].sport, dport= oldPacket[UDP].dport)\
            /DNS(rd=1,id=oldPacket[DNS].id,qd=DNSQR(qname=oldPacket[DNSQR].qname))
            
            resp = sr1(DNSRequest, verbose=0)
            
            respTarget = IP(src=oldPacket[IP].dst, dst=oldPacket[IP].src)\
            /UDP(sport=oldPacket[UDP].dport, dport=oldPacket[UDP].sport)/DNS()
            respTarget[DNS] = resp[DNS]
            send(respTarget, verbose=0)

    def generate_tcp():
        if(oldPacket[TCP].flags == 2):
            if(oldPacket[Ether].src != globalVars.victimArp.MACAddress):
                print(1)
            print(oldPacket[TCP].flags)
            tcpSRequest =\
            IP(src=oldPacket[IP].src, dst=oldPacket[IP].dst)\
            /TCP(sport=oldPacket[TCP].sport, dport=oldPacket[TCP].dport\
            , seq=oldPacket[TCP].seq, window=oldPacket[TCP].window, options=oldPacket[TCP].options)

            resp = sr1(tcpSRequest, verbose=0)
            
            respTargetSA =IP(src=oldPacket[IP].dst, dst=oldPacket[IP].src)\
            /TCP(sport=oldPacket[TCP].dport, dport=oldPacket[TCP].sport\
            , seq=resp[TCP].seq, ack=resp[TCP].ack, flags=resp[TCP].flags, window=resp[TCP].window, options=resp[TCP].options)

            resp = sr1(respTargetSA)
            resp.show()



    if not(ARP in oldPacket or IPv6 in oldPacket):
        if(DNS in oldPacket):
            generate_dns()
        elif(TCP in oldPacket):
            generate_tcp()
        elif(UDP in oldPacket):
            if(NBNSQueryRequest in oldPacket):
                t=1
            elif(oldPacket[UDP].payload.name != "Raw"):
                oldPacket.show()
        else:
            oldPacket.show()