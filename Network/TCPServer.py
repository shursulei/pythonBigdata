#!/usr/bin/env python
import socket
host=''
port=51423
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SQL_SOCKET,socket.SO_REUSEADDR,1)
s.bind("127.0.0.1",port)
s.listen(1)
while 1:
    clientsock,clientaddr = s.accept()
    print("Got connect from",clientsock.getpeername())
    clientsock.close()