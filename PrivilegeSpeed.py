#!/usr/bin/env python
# coding:utf-8

import os
import re
import sys
import time
import threading

# 初始化

sep       = os.sep
root      = os.getcwd()
files     = []
threads   = []
result    = []
viewsType = ['attributeview', 'analyticview', 'calculationview']

viewDir   = { 'attributeview'   : 0 ,
              'analyticview'    : 1,
              'calculationview' : 2 }

# 获取所有文件(AT, AV, CV)
def getFiles(path):
    for (dirname, subdir, subfile) in os.walk(path):
        # print('[' + dirname + ']')
        for f in subfile:
            ExtType = f[f.index('.') + 1 :]  # 获取文件扩展名
            if ExtType in viewsType :
              files.append(os.path.join(dirname, f))


# 删除权限标志
def SetPrivilegeBlank(file, type):
    ViewMapper = {
        0: r'applyPrivilegeType="NONE"',  # attribute   view
        1: r'applyPrivilegeType="NONE"',  # analytic    view
        2: r'applyPrivilegeType="NONE"'   # calculation view
    };

    try:
        with open(file, 'r') as fpr:
            lines = fpr.readlines()
            words = "".join(lines)
            # print('result:', words)
            # searchwords = re.search('privilegeFlag(\s)*="(.*?)(\s)*"', words, flags=re.S)
            # if searchwords:
            #  print(searchwords.group())
            # print(words)
            words = re.sub('applyPrivilegeType(\s)*=(\s)*"(.*?)"', ViewMapper.get(type), words, count=1, flags=re.S)
            # print(words)
        with open(file, 'w') as fpw:
            fpw.writelines(words)
        result.append(file + ' done!')
    except Exception as e:
        print(e)


if __name__ == '__main__':

    # 记录开始时间
    startTime = time.clock()
    getFiles(root)


    #多进程文件读写造成文件丢失 挂起

    # setup multi-thread
    for file in files:
        type = viewDir.get(file[file.index('.') + 1 :])
        # print(file, ":", type)
        task = threading.Thread(target=SetPrivilegeBlank, args=(file, type))
        threads.append(task)

    # run
    for td in threads:
        td.setDaemon(True)
        td.start()


    # 记录结束时间
    EndTime = time.clock()

    for rt in result:
        print(rt)

    print('all done! cost %f s' % (EndTime - startTime))