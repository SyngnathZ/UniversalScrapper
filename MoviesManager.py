#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re
import getopt
import sys

from getFromTMDB import getMVFromTMDB


def get_allMV(dir):
    print('开始获取待修改的电影...')
    for parent, dirNames, fileNames in os.walk(dir):
        for name in fileNames:
            ext = ['.mp4', '.mkv']
            if name.endswith(tuple(ext)):
                incorrectformat_MV(parent, name)


def incorrectformat_MV(dir, filename):
    movie = {'name': '', 'year': ''}  # 初始化一个字典便于后续处理
    namelist = []
    namelist.append(filename.split('.'))  # 将文件名按照.符号进行分割

    if len(namelist[0][0].split(' ')) >= 2:  # 如果文件名的第一项用空格分割是个长度超过1的list，那么则可以认为该文件用空格分割
        namelist[0][0] = filename.split(' ')  # 将文件名按照空格进行分割
        namelist[0][0][-1] = namelist[0][0][-1][:-4]  # 删除被分割出来的文件格式名
        namelist[0][0].append(filename[-3:])  # 将最后后缀加上文件格式名
        del namelist[0][1:]  # 删除多余的list
        namelist = [token for st in namelist for token in st]  # 对结果降维

    # 文件年份判断操作
    i = 0
    for l in namelist[0]:
        match = re.match(r'.*([1-3][0-9]{3})', l)  # 匹配文件名中的年份
        if match is not None:
            movie['name'] = " ".join(namelist[0][:i])  # 默认年份前一个元素为名称
            movie['year'] = namelist[0][i]
            newname = getMVFromTMDB(movie['name'], movie['year'])
            if newname != None:  # 若找到了新的名字
                del namelist[0][i + 1:-1]
                del namelist[0][:i]
                namelist[0].insert(0, newname)
                break
            else:
                for l in namelist[0][i + 1:-1]:
                    if namelist[0][i + 1][0] == '[' and namelist[0][i + 1][-1] == ']':
                        break
                    namelist[0][i + 1] = '[' + l + ']'
                    i += 1
                break
        else:
            i += 1

    replace_filename(dir, filename, filename, ".".join(namelist[0]))  # 进入更名步骤


def replace_filename(dir, file_name, oldPartName, newPartName, Mode=True, err_counter=0):
    try:
        if Mode:
            os.rename(os.path.join(dir, file_name),
                      os.path.join(dir, file_name.replace(oldPartName, newPartName)))  # 进行部分替换
            print('new file name is {0}'.format(file_name.replace(oldPartName, newPartName)))  # 输出替换后的名字
        else:
            os.rename(os.path.join(dir, file_name),
                      os.path.join(dir, file_name.replace(oldPartName, newPartName + oldPartName)))  # 进行部分替换
            print('new file name is {0}'.format(file_name.replace(oldPartName, newPartName + oldPartName)))  # 输出替换后的名字
    except:
        err = err_counter + 1
        tmpNamelist = newPartName.split('.')
        tmpNamelist.insert(2, '[' + str(err) + ']')
        newPart = ".".join(tmpNamelist)
        replace_filename(dir, file_name, oldPartName, newPart, Mode, err_counter=err)


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

    get_allMV(pathstr)


if __name__ == "__main__":
    main(sys.argv[1:])
