#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import getopt
import sys
from TVScrapper.tools.preprocess import find_adj_TV, find_adj_TVwithskip


def get_allTV(dir):
    print('开始获取待修改的影集...')
    for tvlist in os.listdir(dir):
        medianame = []
        for each in os.listdir(os.path.join(dir, tvlist)):  # 获取二级目录下的视频文件
            mediaext = ['.mkv', '.mp4', '.ts', '.ass', '.srt']  # 利用二级目录下的视频文件进行搜索（同时操作字幕）
            if each.endswith(tuple(mediaext)):  # 获取二级目录下的nfo文件
                medianame.append(each)
        find_adj_TVwithskip(medianame, tvlist, dir)  # 获取失败的剧集内容首先跳过处理

    for tvlist in os.listdir(dir):
        medianame = []
        for each in os.listdir(os.path.join(dir, tvlist)):  # 获取二级目录下的视频文件
            mediaext = ['.mkv', '.mp4', '.ts', '.ass', '.srt']  # 利用二级目录下的视频文件进行搜索（同时操作字幕）
            if each.endswith(tuple(mediaext)):  # 获取二级目录下的nfo文件
                medianame.append(each)
        find_adj_TV(medianame, tvlist, dir)  # 将获取到的文件名输入list,获取子文件夹名中的季元信息,并且进行文件名修改和移动


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
    main(sys.argv[1:])
