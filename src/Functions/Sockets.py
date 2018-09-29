'''
This file contains the socket functions this program use
'''

import socket

from KameneCustom.Arp import ArpObj

def start_socket_thread(globalVars, gatewayArp: ArpObj, victimArp: ArpObj):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(('', 80))
    except socket.error as e:
        print(str(e))

    s.listen(10)

    conn, addr = s.accept()

    print('Connected with ' + addr[0] + ':' + str(addr[1]))