#encoding:utf-8
from PropertiesUtil import Properties
import crontba2
import sys,os
import time
from utils.logger import Logger


def getFiles(dir, suffix):  # 查找根目录，文件后缀
    res = []
    for root, directory, files in os.walk(dir):  # =>当前根,根下目录,目录下的文件
        for filename in files:
            name, suf = os.path.splitext(filename)  # =>文件名,文件后缀
            if suf == suffix:
                res.append(name)
    return res

if __name__ == '__main__':


    dictProperties=Properties("global.properties").getProperties()
    time_stamp = int(time.time())
    # print time_stamp
    for conf_string,system_command in dictProperties.items():
        res, desc=crontba2.parse_crontab_time(conf_string)
        if res == 0:
            cron_time = desc
        else:
            # print desc
            sys,exit(-1)

        time_struct = crontba2.get_struct_time(time_stamp)
        match_res = crontba2.time_match_crontab(cron_time, time_struct)
        # print  match_res
        if (match_res[1]):
            Logger("running").get_log().debug(system_command)
            os.system("su - wedwah -c 'system_command' ");
