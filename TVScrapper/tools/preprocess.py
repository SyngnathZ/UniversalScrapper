#!/usr/bin/python
# -*- coding: UTF-8 -*-

import platform
import re
import os
import shutil
import xml.etree.ElementTree as ET
from tmdbv3api import TMDb
from tmdbv3api import Movie, TV
from getFromTMDB import getTVFromTMDB, getTVFromTMDB_withskip

tmdb = TMDb()
tmdb.api_key = '8a93c641a109bafadb38b526e7b2bb56'
tmdb.language = 'zh'


def find_adj_TV(filename, tvname, rootdir):
    passkey = False
    TV_Season = ''
    namelist = []
    for each in filename:
        each = each.replace(' ', '.')  # 将所有空格替换成句点
        namelist.append(each.split('.'))  # 首先用.进行分割
    # 将所有空格替换成点号
    TV_name = dict()
    TV_name['old'] = filename
    TV_name['SeriesYear'] = 'UNKONWN'
    TV_name['SeriesName'] = None

    j = 0
    for _ in namelist[0]:
        # 初步检查是否包含季元信息
        match = re.match(r'.*([S,s][0-9]{2})', namelist[0][j])  # 匹配文件名中的季度信息
        if match is not None:
            TV_Season = namelist[0][j]
            break
        j += 1  # 以j作为季元信息的对比符号

    k = 0
    for _ in namelist[0]:
        # 初步检查是否包含季元信息
        match = re.match(r'.*([1-3][0-9]{3})', namelist[0][k])  # 查看倒数第二位是否匹配文件名中的年份
        if match is not None and k != 0:
            TV_name['SeriesYear'] = namelist[0][k]
            break
        k += 1  # 以j作为季元信息的对比符号

    i = 0
    # 如果只有一集的情况，进行部分人工预处理
    if len(namelist[:][:]) == 1:
        for num in range(len(namelist[0])):
            print('第' + str(num) + '是：' + namelist[0][num])
        TV_name_num = input("表示该剧集名称的最后一个字符串号: ")
        TV_ep_num = input("表示该剧集集数的字符串号: ")
        if j == len(namelist[0]):
            TV_Season = 'S' + str(input("请输入" + tvname + "的季号(01、02、03...记得带0)，直接回车则默认为01: "))  # 搜索失败则人工干预
        else:
            TV_Season = namelist[0][j][:3]  # 如果剧集分集上即能获取季元数据
        if TV_Season == 'S':
            print('使用默认值S01...')
            TV_Season = 'S01'
        passkey = True  # 跳过检查
        TV_name['SeriesName'] = ' '.join(namelist[0][:int(TV_name_num) + 1])  # 准确获取年份
        i = int(TV_ep_num)

    for _ in namelist[0]:
        # 初步检查是否包含季元信息
        if passkey or namelist[0][i] != namelist[1][i]:  # 遍历所有拆开的字符串
            if i > j:  # 如果剧季信息为单独出现，则需要进行不太一样的操作（这段有点复杂）
                for num in range(len(namelist)):
                    del namelist[num][j]
                i = i - 1  # 剔除季元信息后对其他关键文件名造成的影响
                if k > j:
                    k = k - 1
            if i > k:
                for num in range(len(namelist)):
                    del namelist[num][k]
                i = i - 1
            if TV_name['SeriesName'] is None:
                TV_name['SeriesName'] = ' '.join(namelist[0][:i])  # 无年份干扰
            TV_name['SeriesName'], TV_name['SeriesYear'] = getTVFromTMDB(TV_name['SeriesName'], rootdir, tvname)
            if 'S' in namelist[0][i]:
                TV_name['new'] = []
                TV_Season = namelist[0][i][:3]  # 如果剧集分集上即能获取季元数据
                for num in range(len(namelist)):
                    TV_name['new'].append(".".join(namelist[num]))  # 记录新文件名
                move_success(rootdir, tvname, TV_name, TV_Season)
                return
            else:
                incorrect = ['ep', 'e', 'Ep']  # 列出所有不合理的关于E0x的命名方法
                for each in incorrect:
                    if each in namelist[0][i]:
                        for num in range(len(namelist)):
                            namelist[num][i] = namelist[num][i].replace(each, 'E')
                # 如果子文件夹里的媒体文件不包含季度信息，则进入季元信息获取
                if TV_Season == '':  # 若前面过程在剔除季元信息过程中获得了季信息则跳过
                    TV_Season = get_Seasoninfo(tvname)

                if TV_Season != None:  # 如果通过母文件夹名获取成功则直接利用季元信息
                    incorrect = ['s']  # 列出所有不合理的关于S0x的命名方法
                    for each in incorrect:
                        TV_Season = TV_Season.replace(each, 'S')
                else:
                    TV_Season = 'S' + str(input("请输入" + tvname + "的季号(01、02、03...记得带0)，直接回车则默认为01: "))  # 搜索失败则人工干预
                    if TV_Season == 'S':
                        print('使用默认值S01...')
                        TV_Season = 'S01'

                TV_name['new'] = []
                for num in range(len(namelist)):
                    namelist[num][i] = TV_Season + namelist[num][i]
                    TV_name['new'].append(".".join(namelist[num]))  # 记录新文件名

                # 进行改名操作，文件名添加
                for num in range(len(namelist)):
                    replace_filename(os.path.join(rootdir, tvname), TV_name['old'][num], TV_name['old'][num],
                                     TV_name['new'][num])  # 改名操作
                move_success(rootdir, tvname, TV_name, TV_Season)
                return

        i += 1


def find_adj_TVwithskip(filename, tvname, rootdir):  # 将人工处理的部分剔除，跳过人工处理的部分
    passkey = False
    TV_Season = ''
    namelist = []
    for each in filename:
        each = each.replace(' ', '.')  # 将所有空格替换成句点
        tmp = each.split('.')
        tmp = [i for i in tmp if i != '']  # 去除空值
        namelist.append(tmp)  # 首先用.进行分割

    # 将所有空格替换成点号
    TV_name = dict()
    TV_name['old'] = filename
    TV_name['SeriesYear'] = 'UNKONWN'
    TV_name['SeriesName'] = None

    j = 0
    for _ in namelist[0]:
        # 初步检查是否包含季元信息
        match = re.match(r'.*([S,s][0-9]{2})', namelist[0][j])  # 匹配文件名中的季度信息
        if match is not None:
            TV_Season = namelist[0][j]
            break
        j += 1  # 以j作为季元信息的对比符号

    k = 0
    for _ in namelist[0]:
        # 初步检查是否包含季元信息
        match = re.match(r'.*([1-3][0-9]{3})', namelist[0][k])  # 查看倒数第二位是否匹配文件名中的年份
        if match is not None and k != 0:
            TV_name['SeriesYear'] = namelist[0][k]
            break
        k += 1  # 以j作为季元信息的对比符号

    i = 0
    # 如果只有一集的情况，首先跳过，后续过程将参与预处理
    if len(namelist[:][:]) == 1:
        print(tvname + '只有一集，跳过......')
        return None

    for _ in namelist[0]:
        # 初步检查是否包含季元信息
        if passkey or namelist[0][i] != namelist[1][i]:  # 遍历所有拆开的字符串
            if i > j:  # 如果剧季信息为单独出现，则需要进行不太一样的操作（这段有点复杂）
                for num in range(len(namelist)):
                    del namelist[num][j]
                i = i - 1  # 剔除季元信息后对其他关键文件名造成的影响
                if k > j:
                    k = k - 1
            if i > k:
                for num in range(len(namelist)):
                    del namelist[num][k]
                i = i - 1
            if TV_name['SeriesName'] is None:
                TV_name['SeriesName'] = ' '.join(namelist[0][:i])  # 无年份干扰
            TV_name['SeriesName'], TV_name['SeriesYear'] = getTVFromTMDB_withskip(TV_name['SeriesName'], rootdir,
                                                                                  tvname)
            if TV_name['SeriesName'] == 'Skip':  # 跳过判断
                return

            if 'S' in namelist[0][i]:
                TV_name['new'] = []
                TV_Season = namelist[0][i][:3]  # 如果剧集分集上即能获取季元数据
                for num in range(len(namelist)):
                    TV_name['new'].append(".".join(namelist[num]))  # 记录新文件名
                move_success(rootdir, tvname, TV_name, TV_Season)
                return
            else:
                incorrect = ['ep', 'e', 'Ep']  # 列出所有不合理的关于E0x的命名方法
                for each in incorrect:
                    if each in namelist[0][i]:
                        for num in range(len(namelist)):
                            namelist[num][i] = namelist[num][i].replace(each, 'E')
                # 如果子文件夹里的媒体文件不包含季度信息，则进入季元信息获取
                if TV_Season == '':  # 若前面过程在剔除季元信息过程中获得了季信息则跳过
                    TV_Season = get_Seasoninfo(tvname)

                if TV_Season != None:  # 如果通过母文件夹名获取成功则直接利用季元信息
                    incorrect = ['s']  # 列出所有不合理的关于S0x的命名方法
                    for each in incorrect:
                        TV_Season = TV_Season.replace(each, 'S')
                else:
                    print(tvname + '找不到对应信息，跳过......')
                    return None

                TV_name['new'] = []
                for num in range(len(namelist)):
                    namelist[num][i] = TV_Season + namelist[num][i]
                    TV_name['new'].append(".".join(namelist[num]))  # 记录新文件名

                # 进行改名操作，文件名添加
                for num in range(len(namelist)):
                    replace_filename(os.path.join(rootdir, tvname), TV_name['old'][num], TV_name['old'][num],
                                     TV_name['new'][num])  # 改名操作
                move_success(rootdir, tvname, TV_name, TV_Season)
                return

        i += 1


def find_diynfo(source):
    tv = Movie()
    with open(source, 'r', encoding='ISO-8859-1') as f:
        for line in f.readlines():
            if 'imdb.com' in line:  # 通过nfo找imdb_tt
                imdb_id = line.split('/')[-2]
                search = tv.external(imdb_id, 'imdb_id')  # 输入电影名查询
                try:
                    if len(search.tv_results) != 0:
                        TV_name = search.tv_results[0].name  # 获取名字
                        TV_year = search.tv_results[0].first_air_date[:4]  # 获取年份
                    elif len(search.tv_episode_results) != 0:
                        TVshow_id = search.tv_episode_results[0].show_id  # 获取名字
                        tv_series = TV()
                        tv_results = tv_series.details(TVshow_id)
                        TV_name = tv_results.name  # 获取名字
                        TV_year = tv_results.first_air_date[:4]  # 获取年份
                    return TV_name, TV_year
                except:
                    print(source, '没找到!!')
                    return None


def find_standardnfo(source):
    tree = ET.parse(source)
    movie = tree.getroot()

    TV_name = movie[0].text  # title
    TV_year = movie[4].text  # year
    return TV_name, TV_year


def get_Seasoninfo(tvname):
    tvname = tvname.replace(' ', '.')  # 将所有空格替换成句点
    namelist = tvname.split('.')  # 用.进行分割
    for l in namelist:
        match = re.match(r'.*([S,s][0-9]{2})', l)  # 匹配文件名中的季度信息
        if match is not None:
            return l

    return None  # 若没找到季元信息


def replace_filename(dir, file_name, oldPartName, newPartName, afterdir=None, Mode=True, err_counter=0):
    try:
        if Mode:
            os.rename(os.path.join(dir, file_name),
                      os.path.join(dir, file_name.replace(oldPartName, newPartName)))  # 进行部分替换
            print('new file name is {0}'.format(file_name.replace(oldPartName, newPartName)))  # 输出替换后的名字
            if afterdir != None:
                src = os.path.join(dir, newPartName)
                dst = os.path.join(afterdir, newPartName)
                shutil.move(src, dst)  # 将获取失败的文件统一挪动到指定文件夹
        else:
            os.rename(os.path.join(dir, file_name),
                      os.path.join(dir, file_name.replace(oldPartName, newPartName + oldPartName)))  # 进行部分替换
            print('new file name is {0}'.format(file_name.replace(oldPartName, newPartName + oldPartName)))  # 输出替换后的名字
    except FileExistsError:
        err = err_counter + 1
        tmpNamelist = newPartName.split('.')
        tmpNamelist.insert(2, '[' + str(err) + ']')
        newPart = ".".join(tmpNamelist)
        replace_filename(dir, file_name, oldPartName, newPart, Mode=Mode, err_counter=err)


def getlastLevel_success(dir):  # 返回上二层级刮削成功文件夹
    if platform.system().lower() == 'windows':
        dirlist = dir.split('\\')
        del dirlist[-2:]  # 删除两层文件夹层级
        return '\\'.join(dirlist) + '\\刮削成功'
    elif platform.system().lower() == 'linux' or platform.system().lower() == 'darwin':
        dirlist = dir.split('/')
        del dirlist[-2:]
        return '/'.join(dirlist) + '/刮削成功'


def move_success(rootdir, tvname, TV_name, TV_Season):
    src = os.path.join(rootdir, tvname)
    TV_name['SeriesName'] = validateTitle(TV_name['SeriesName'])
    if TV_name['SeriesYear'] != 'UNKONWN':
        dst = os.path.join(getlastLevel_success(src),
                           TV_name['SeriesName'] + ' (' + TV_name['SeriesYear'] + ')')
    else:  # 若没搜索到年份信息，则空余年份信息
        dst = os.path.join(getlastLevel_success(src), TV_name['SeriesName'])
    mkdirs(dst)  # 首先创建文件夹
    shutil.move(src, dst)  # 将获取失败的文件统一挪动到指定文件夹
    try:
        os.rename(os.path.join(dst, tvname), os.path.join(dst, TV_Season.replace('S', 'Season ')))
    except OSError:
        print('存在相同分辨率文件夹，合并中...')
        change(os.path.join(dst, tvname), os.path.join(dst, TV_Season.replace('S', 'Season ')))
        os.rmdir(os.path.join(dst, tvname))
    return


def mkdirs(path):
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


def validateTitle(title):  # 非法字符判断
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, ".", title)  # 替换为下划线
    return new_title


def change(path, path1):  # 将一个文件夹里的内容移动到另一个文件夹
    for f in os.listdir(path):
        if os.path.isfile(path + os.path.sep + f):
            shutil.move(path + os.sep + f, path1)
        elif os.path.isdir(path + os.path.sep + f):
            change(path + os.sep + f, path1)
