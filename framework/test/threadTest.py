#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/21 16:50
# @Author  : shursulei
# @Site    : 
# @File    : threadTest.py
# @Software: PyCharm
# @describe:
'''
import time
import threading

class myThread(threading.Thread):
    def __init__(self,n):
        threading.Thread.__init__(self)
        self.myThread_n=n
    def run(self):
        global count
        for i in range(self.myThread_n):
            if lock.acquire():
                _Temp=count
                time.sleep(0.0001)
                count=_Temp+1
                lock.release()
def func(n):
    global  count
    time.sleep(0.1)
    for i in range(n):
        count+=1

if __name__ == '__main__':
    count=0
    lock=threading.Lock()
    threads=[]
    for i in range(5):
        threads.append(myThread(1000))
    for t in threads:
        print(t.getName())
        t.start()
    time.sleep(5)
    print('count:',count)
