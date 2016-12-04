#!/usr/bin/env python
# coding:utf-8

import os
import re
import sys
import time
import threading

# 初始化

sep       = os.sep
root      = os.getcwd() # r"C:\Users\i321482\Desktop\exp"
files     = []
threads   = []
result    = []
viewsType = ['attributeview', 'analyticview', 'calculationview']

viewDir   = { 'attributeview'   : 0 ,
              'analyticview'    : 1,
              'calculationview' : 2
            };

ViewMapper = { 0: r'applyPrivilegeType="NONE"',  # attribute   view
               1: r'applyPrivilegeType="NONE"',  # analytic    view
               2: r'applyPrivilegeType="NONE"'   # calculation view
             };

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


    try:
        with open(file, 'r', encoding = 'gbk') as fpr:
            lines = fpr.readlines()
            words = "".join(lines)
            # searchwords = re.search('privilegeFlag(\s)*="(.*?)(\s)*"', words, flags=re.S)
            # if searchwords:
            #  print(searchwords.group())
            # print(words)
            words = re.sub('applyPrivilegeType(\s)*=(\s)*"(.*?)"', ViewMapper.get(type), words, count=1, flags=re.S)
            # print(words)
        with open(file, 'w', encoding = 'gbk') as fpw:
            fpw.writelines(words)
        result.append(file + ' done!')
    except Exception as e:
        print(e)


if __name__ == '__main__':

    # 记录开始时间
    startTime = time.clock()
    getFiles(root)

    for file in files:
        type = viewDir.get(file[file.index('.') + 1:])
        print(file, ":", type)
        SetPrivilegeBlank(file, type)

    # 记录结束时间
    EndTime = time.clock()

    for rt in result:
        print(rt)

    print('all done! cost %f s' % (EndTime - startTime))