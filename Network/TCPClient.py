#!/usr/bin/env python
import socket
print("Creating socket...")
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
print("done.")
print("Looking up port number...")
port=socket.getservbyname('http','tcp')
print(port)
print("done.")
print("Connecting to remote host ...")
s.connect(("www.baidu.com",port))
print("done.")
print("Connected from ",s.getsockname())#获取发送的ip和端口
print("Connected to",s.getpeername())#获取目的地的IP和端口