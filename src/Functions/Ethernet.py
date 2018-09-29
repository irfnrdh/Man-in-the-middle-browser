'''
This file contains the ethernet functions this program use
'''

import os

from Functions.Terminal import get_terminal_lines
from Functions.Arrays import get_phrase_from_list, split_list_by_phrase

from KameneCustom.Interfaces import get_my_default_iface

def get_ethernet_interfaces():
    if(os.name == "nt"): #windows
        terminalLog = get_terminal_lines(CMD='arp -a')
        terminalLog = get_phrase_from_list(terminalLog, 'Interface')
        terminalLog = split_list_by_phrase(terminalLog, ' ', 1)
    elif(os.name == "posix"): #linux
        terminalLog = get_terminal_lines(CMD='ifconfig')
        terminalLog = get_phrase_from_list(terminalLog, 'inet ')
        terminalLog = split_list_by_phrase(terminalLog, 'inet ', 1)
        terminalLog = split_list_by_phrase(terminalLog, ' ', 0)
    return(terminalLog)

def get_arp_table(interface = ""):
    if(os.name == "nt"): #windows
        if(interface == ""):
            terminalLog = get_terminal_lines(CMD='arp -a')
        else:
            terminalLog = get_terminal_lines(CMD='arp -a -N '+interface)

        specificLog = get_phrase_from_list(terminalLog, 'dynamic')
        specificLog.extend(get_phrase_from_list(terminalLog, 'static'))

        ipAddresses = split_list_by_phrase(specificLog, '  ', 1)
        macAddresses = split_list_by_phrase(split_list_by_phrase(specificLog, '     ', -2), ' ', -1)
        
    elif(os.name == "posix"): #linux
        if(interface == ""):
            terminalLog = get_terminal_lines(CMD='arp -a')
        else:
            interfaceName = str(get_terminal_lines(CMD=[['ifconfig'], ['grep', '-B1', '10.0.0.11']])).split(':')[0]
            terminalLog = get_terminal_lines(CMD=['arp', '-a', '-i', interfaceName])
            ipAddresses = split_list_by_phrase(split_list_by_phrase(terminalLog, '(', 1), ')', 0)
            macAddresses = split_list_by_phrase(split_list_by_phrase(terminalLog, 'at ', 1), ' ', 0)

    arpList = []
    for i in range(0, len(ipAddresses)):
            arp = ipAddresses[i] + " - " + macAddresses[i].replace('-', ':')
            arpList.append(arp)
    return(arpList)
