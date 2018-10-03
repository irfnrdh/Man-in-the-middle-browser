#filter='tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420' -> http get

from kamene.all import sniff, sr1
from kamene.layers.dns import Raw, Packet

import threading
import matplotlib.pyplot

packets = []
stop = False

def packet_get(packet: Packet):
    packets.append(packet)
    print(str(len(packets)))
    #recv = sr1(packet)


def checkStop():
    return stop

def sniffFunc():
    sniff(filter='tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420 and src host 10.0.0.12' , prn = packet_get, store=0, stop_callback=checkStop)

if __name__ == '__main__':
    thread_sniff = threading.Thread(target=sniffFunc)
    thread_sniff.start()
    while True:
        print('write - stop\n')
        if(input("") == "stop"):
            stop= True
            for i in range(0, len(packets)):
                print("###############"+str(i))
                packets[i].show()
                print('\n\n\n\n')
            break

    
