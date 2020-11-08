from multiprocessing import Process, Queue
import os, time, random


# 写数据的进程
def write(q):
    print('写进程PID：%s' % os.getpid())
    for value in ['I', 'Love', 'Python']:
        print('放入队列：%s，时间：%s' % (value, time.time()))
        q.put(value)
        time.sleep(random.random())


# 读数据的进程：
def read(q):
    print('读进程PID：%s' % (os.getpid()))
    while True:
        value = q.get(True)
        print('获得数据：%s，时间：%s' % (value, time.time()))


if __name__ == '__main__':
    # 父进程创建Queue，并传给各个子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()
    pr.start()
    pw.join()
    pr.terminate()  # pr进程是死循环，无法等待其结束，只能强行终止