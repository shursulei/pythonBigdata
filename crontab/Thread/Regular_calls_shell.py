#!/user/bin/env python
'''
循环调用该脚本
'''
import time,os,sched
def re_exe(cmd,inc=120):
    while True:
        os.system(cmd)
        time.sleep(inc)
re_exe("sh amc_sasshare.sh",120)
# 执行该脚本可以使用 python xxx.py &
#unhup python 文件名.py (> ***.log )&
'''
sched调度
'''
s=sched.scheduler(time.time,time.sleep)
def perform_fun(cmd):
    os.system(cmd)
def run_shell():
    s.enter(120,1,perform_fun(),("./amc_sasshare.sh",))
    s.run()
if __name__=='main':
    run_shell()
try:
    s.empty()
except:
    raise ValueError

#!/user/bin/env python
#@File   :PerformTaskTimer.py
import time,os,sched
schedule = sched.scheduler(time.time,time.sleep)
def perform_command(cmd,inc):
  #在inc秒后再次运行自己，即周期运行
  schedule.enter(inc, 0, perform_command, (cmd, inc))
  os.system(cmd)
def timming_exe(cmd,inc=60):
  schedule.enter(inc,0,perform_command,(cmd,inc))
  schedule.run()#持续运行，直到计划时间队列变成空为止
print('show time after 2 seconds:')
timming_exe('echo %time%',2)