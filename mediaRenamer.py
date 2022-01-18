#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re


# 遍历文件夹及其子文件夹中的文件，并存储在一个列表中
# 输入文件夹路径、空文件列表[]
# 返回 文件列表Filelist,包含文件名（完整路径）
def get_alldir(dir):
    newDir = dir
    if os.path.isdir(dir):
        for s in os.listdir(dir):
            if s.endswith(('.mp4', '.mkv')):
                print(dir)
                incorrectformat(dir)
                break
            newDir = os.path.join(dir, s)
            get_alldir(newDir)


def incorrectformat(dir):
    namelist = []
    for file_name in os.listdir(dir):  # 取出文件夹下各文件名（包括子文件中的）
        if file_name.endswith(('.mp4', '.mkv')):  # 选出要修改的文件类型；此句取消后就不对类型做判断
            namelist.append(file_name.split('.'))  # 将文件名按照.符号进行分割

    if len(namelist[:][:]) == 1:  # 判断是否只有一个文件，若只有一个文件则需要手动输入编号
        pass  # 手动输入
    else:
        i = 0
        for _ in namelist[0]:
            if namelist[0][i] != namelist[1][i]:  # 遍历所有拆开的字符串
                if 'S' in namelist[0][i]:
                    print('正常')
                    return
                else:
                    break
            else:
                i += 1

        print('不正常')
        addstr = input("请输入需要重命名的季号: ")
        addstr = 'S' + str(addstr)
        for each in namelist[:]:
            replace_filename(dir, ".".join(each), each[i], addstr, False)


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

    # 文件年份判断操作
    i = 0
    for l in namelist[0]:
        match = re.match(r'.*([1-3][0-9]{3})', l)
        if match is not None:
            break
        else:
            i += 1

    for l in namelist[0][i + 1:-1]:
        namelist[0][i + 1] = '[' + l + ']'
        i += 1

    replace_filename(dir, filename, filename, ".".join(namelist[0]))


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
    funcscl = input("请选择要做的事情，1为电影正常化改名，2为电视剧改名: ")
    if funcscl == '1':
        pathstr = input("请输入需要检查的文件夹地址: ")
        get_allMV(pathstr)
    if funcscl == '2':
        pathstr = input("请输入需要检查的文件夹地址: ")
        get_alldir(pathstr)
