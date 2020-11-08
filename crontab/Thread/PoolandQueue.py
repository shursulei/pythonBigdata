import os, time, random
from multiprocessing import Pool


def task(name):
    print('正在运行的任务：%s，PID：（%s）' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 10)
    end = time.time()
    print('任务：%s，用时：%0.2f 秒' % (name, (end - start)))


if __name__ == '__main__':
    print('父进程ID：%s' % (os.getpid()))
    p = Pool(4)
    for i in range(5):
        p.apply_async(task, args=(i,))
    print('等待所有添加的进程运行完毕。。。')
    p.close()  # 在join之前要先关闭进程池，避免添加新的进程
    p.join()
    print('End!!,PID:%s' % os.getpid())