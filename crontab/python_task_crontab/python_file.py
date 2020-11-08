# -*- coding:utf-8 -*-
import os

if __name__ == '__main__':
    def getFiles(dir, suffix):  # 查找根目录，文件后缀
        res = []
        for root, directory, files in os.walk(dir):  # =>当前根,根下目录,目录下的文件
            for filename in files:
                name, suf = os.path.splitext(filename)  # =>文件名,文件后缀
                if suf == suffix:
                    res.append(name)
                    #print name
                    # res.append(os.path.join(root, filename))  # =>吧一串字符串组合成路径
        return res
for file in getFiles("./", '.properties'):
    user=file[len("global_"):len(file)].replace("\n", "")
    properties_file=file+"properties"
    # if user is not None and properties_file is not None:
#     f = open("user.ini", "r")
#     lines = f.readlines()
#     for line in lines:
#         for file in getFiles("./", '.properties'):
#             print  file
#             user_ini=line.replace("\n", "")
#             user_properties=file[len("global_"):len(file)]
#             if user_ini == user_properties:
#                 print user_properties
#                 print  file

