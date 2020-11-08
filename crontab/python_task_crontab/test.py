from PropertiesUtil import Properties
import crontba2
import sys,os
import time
from utils.logger import Logger
if __name__ == '__main__':

    dictProperties=Properties("global.properties").getProperties()
    time_stamp = int(time.time())
    for i,j in dictProperties.items():
        res, desc=crontba2.parse_crontab_time(i)
        if res == 0:
            cron_time = desc
        else:
            print desc
            sys,exit(-1)
        print "\nparse result(range for crontab):"
        print " minute:", cron_time[0]
        print " hour: ", cron_time[1]
        print " day: ", cron_time[2]
        print " month: ", cron_time[3]
        print " week day:", cron_time[4]
        time_struct = crontba2.get_struct_time(time_stamp)
        print "\nstruct time(minute hour day month week) for %d :" % \
              time_stamp, time_struct
        match_res = crontba2.time_match_crontab(cron_time, time_struct)
        print "\nmatching result:", match_res[1]
        most_close = crontba2.close_to_cron(cron_time, time_struct)
        print "\nin range of crontab time which is most colse to struct ", most_close
        time_list = crontba2.cron_time_list(cron_time)
        print "\n\n %d times need to tart-up:\n" % len(time_list)
        print time_list

        print i,":",j
        os.system(j)
