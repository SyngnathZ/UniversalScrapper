#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re


def get_allMV(dir):
    print('开始获取待修改的电影...')
    for parent, dirNames, fileNames in os.walk(dir):
        for name in fileNames:
            ext = ['.mp4', '.mkv']
            if name.endswith(tuple(ext)):
                print(fileNames)
                incorrectformat_MV(parent, name)


def incorrectformat_MV(dir, filename):
    namelist = []
    namelist.append(filename.split('.'))  # 将文件名按照.符号进行分割

    if len(namelist) == 1:  # 如果文件名是用空格分隔
        namelist[0] = (filename.split(' '))  # 将文件名按照.空格进行分割

    # 文件年份判断操作
    i = 0
    match = None
    for l in namelist[0]:
        match = re.match(r'.*([1-3][0-9]{3})', l)  # 匹配文件名中的年份
        if match is not None:
            break
        else:
            i += 1

    if match is not None:
        for l in namelist[0][i + 1:-1]:
            namelist[0][i + 1] = '[' + l + ']'
            i += 1

        replace_filename(dir, filename, filename, ".".join(namelist[0]))  # 进入更名步骤


def replace_filename(dir, file_name, oldPartName, newPartName, Mode=True):
    if Mode:
        os.rename(os.path.join(dir, file_name),
                  os.path.join(dir, file_name.replace(oldPartName, newPartName)))  # 进行部分替换
        print('new file name is {0}'.format(file_name.replace(oldPartName, newPartName)))  # 输出替换后的名字
    else:
        os.rename(os.path.join(dir, file_name),
                  os.path.join(dir, file_name.replace(oldPartName, newPartName + oldPartName)))  # 进行部分替换
        print('new file name is {0}'.format(file_name.replace(oldPartName, newPartName + oldPartName)))  # 输出替换后的名字


if __name__ == '__main__':
    pathstr = input("请输入需要检查的文件夹地址: ")
    get_allMV(pathstr)
