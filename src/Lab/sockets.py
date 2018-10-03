'''
This file contains the socket functions this program use
'''

import socket
import threading
import select
import queue

from kamene.all import sr1
from kamene.layers.l2 import Ether
from kamene.layers.dns import IP, Raw

class SocketServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.inputs = [self.socket]
        self.outputs = []
        self.message_queues = {}
        self.bufferSize = 4096
        self.packets = []

    def bind(self, port, ipAddr = '', listenCount = 1):
        self.socket.bind((ipAddr, port))
        #self.socket.listen(listenCount)
    
    def serverListen(self):
        connection, connAddress = self.socket.accept()
        connection.setblocking(0)
        self.inputs.append(connection)
        self.message_queues[connection] = queue.Queue()

    def dataListen(self, s):
        data = s.recv(self.bufferSize)
        dataLen = len(data)
        if data:
            self.message_queues[s].put(data)
            if s not in self.outputs:
                self.outputs.append(s)
        if not data or dataLen < self.bufferSize:
            if s in self.outputs:
                self.outputs.remove(s)
            self.inputs.remove(s)
            s.close()
            packet = b"".join(self.message_queues[s].queue)
            p = Ether(packet)
            self.packets.append(Ether(packet))
            del self.message_queues[s]

    def startListen(self):
        while self.inputs:
            self.readable, self.writeable, self.expectional = select.select(self.inputs, self.outputs, self.inputs)
            for s in self.readable:
                if s is self.socket:
                    self.serverListen()
                else:
                    self.dataListen(s)

            for s in self.writeable:
                try:
                    next_msg = self.message_queues[s].get_nowait()
                except queue.Empty:
                    self.outputs.remove(s)
                else:
                    s.send(next_msg)

            for sn in self.expectional:
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                del self.message_queues[s]



def start_socket_thread():
    '''datas = ""
    while True:
        data = conn.recv(1024)
        l = len(data)
        if(l < 1024):
            datas += data.decode()
            break
        if not data:
            break
        datas += data.decode()
        conn.sendall(data)
    d = Ether(datas.encode())
    conn.close()'''


if __name__ == '__main__':
    socketServer = SocketServer()
    socketServer.bind(port=9090, listenCount=5)
    socketServer.startListen()