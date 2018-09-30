'''
This file contains the socket functions this program use
'''

import socket
import threading

def start_socket_thread():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(('', 9090))
    except socket.error as e:
        print(str(e))

    s.listen(10)

    conn, addr = s.accept()

    print('Connected with ' + addr[0] + ':' + str(addr[1]))

def demo_send():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('127.0.0.1', 9090))
    s.send(str('hello').encode())
if __name__ == '__main__':
       thread = threading.Thread(target=start_socket_thread)
       thread.start()
       demo_send()