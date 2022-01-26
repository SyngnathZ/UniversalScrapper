#!/usr/bin/python
# -*- coding: UTF-8 -*-

import platform
import os
import re
import getopt
import shutil
import sys
from TVScrapper.tools.preprocess import find_diynfo, find_TVname


def get_allTV(dir):
    print('开始获取待修改的影集...')
    for tvlist in os.listdir(dir):
        # for each in os.listdir(os.path.join(dir, tvlist)):  # 获取二级目录下的视频文件
        #     nfoext = ['.nfo']  # 利用nfo文件进行搜索
        #     if each.endswith(tuple(nfoext)):  # 获取二级目录下的nfo文件
        #         print(find_diynfo(os.path.join(dir, tvlist, each)))

        medianame = []
        for each in os.listdir(os.path.join(dir, tvlist)):  # 获取二级目录下的视频文件
            mediaext = ['.mkv', 'mp4']  # 利用二级目录下的视频文件进行搜索
            if each.endswith(tuple(mediaext)):  # 获取二级目录下的nfo文件
                medianame.append(each)
        TV_Season, offset = find_TVname(medianame, tvlist)  # 将获取到的文件名输入list,获取子文件夹名中的季元信息


def getlastLevel(dir):  # 返回上一层级的文件夹名字
    if platform.system().lower() == 'windows':
        dirlist = dir.split('\\')
        del dirlist[-1]
        return '\\'.join(dirlist) + '\\刮削失败'
    elif platform.system().lower() == 'linux':
        dirlist = dir.split('/')
        del dirlist[-1]
        return '/'.join(dirlist) + '/刮削失败'


def main(argv):
    pathstr = ''
    databaseName = ''
    try:
        opts, args = getopt.getopt(argv, "p:d:", ["path=", "database="])
    except getopt.GetoptError:
        print('-p -d -c ')
        sys.exit()

    for opt, arg in opts:
        if opt in ('-p', ' path'):
            pathstr = arg
        elif opt in ('-d', ' database'):
            databaseName = arg

    get_allTV(pathstr)


if __name__ == "__main__":
    print(platform.system().lower())
    main(sys.argv[1:])
