import os
from imdb import IMDb
from tmdbv3api import TMDb
from tmdbv3api import Movie, TV

tmdb = TMDb()
tmdb.api_key = '8a93c641a109bafadb38b526e7b2bb56'
tmdb.language = 'zh'


def getMVFromTMDB(name, year):
    movie = Movie()
    search = movie.search(name)  # 输入电影名查询

    for res in search:
        try:
            if res.release_date != '':
                if int(year) + 1 >= int(res.release_date[:4]) >= int(
                        year) - 1:  # 通过预知电影年份进行匹配
                    return res.title
        except:
            print('没找到，使用其他方法继续查询......')
            return None

    IMDBid = getMVFromIMDB(name, year)
    search = movie.external(IMDBid, 'imdb_id')  # 输入电影名查询
    try:
        result = search.movie_results[0].title
        return result
    except:
        print(name, '没找到!!')
        return None


def getTVFromTMDB(name, dir, tvlist):
    TV_name = None
    TV_year = None
    tv = TV()
    search = tv.search(name)  # 输入电影名查询

    if len(search) == 1:  # 如果是唯一结果
        for res in search:
            return res.name, res.first_air_date[:4]
    elif len(search) > 1:
        # 如果有多个搜索结果，则首先尝试搜索nfo文件
        from TVScrapper.tools.preprocess import find_diynfo
        for each in os.listdir(os.path.join(dir, tvlist)):  # 获取二级目录下的视频文件
            nfoext = ['.nfo']  # 利用nfo文件进行搜索
            if each.endswith(tuple(nfoext)):  # 获取二级目录下的nfo文件
                TV_name, TV_year = find_diynfo(os.path.join(dir, tvlist, each))
                if TV_name is not None:
                    return TV_name, TV_year
        i = 0
        for res in search:
            try:
                print(str(i) + '是:' + res.name + '，首播日期是' + res.first_air_date)
            except AttributeError:
                print('该选项无效，跳过该选项')  # 避免出现空值导致错误
            i += 1
        print(tvlist)
        num = input("有多个搜索结果，请输入正确的编号: ")
        return search[int(num)].name, search[int(num)].first_air_date[:4]  # 若有多个搜索结果则人工介入
    else:
        # 如果有没有搜索结果，则首先尝试搜索nfo文件
        from TVScrapper.tools.preprocess import find_diynfo
        for each in os.listdir(os.path.join(dir, tvlist)):  # 获取二级目录下的视频文件
            nfoext = ['.nfo']  # 利用nfo文件进行搜索
            if each.endswith(tuple(nfoext)):  # 获取二级目录下的nfo文件
                TV_name, TV_year = find_diynfo(os.path.join(dir, tvlist, each))
                if TV_name is not None:
                    return TV_name, TV_year
        print('找不到该文件夹下的剧集信息，且没有nfo：' + tvlist)
        TV_name = input("请手动查询该剧集名称并输入，若实在搜不到可以直接回车: ")
        TV_year = input("请手动查询该剧集发行年份并输入，若实在搜不到可以直接回车: ")
        if TV_name and TV_year is not None:
            return TV_name, TV_year  # 手动输入
        else:
            return name, 'UNKNOWN'  # 没搜到的情况


def getMVFromIMDB(name, year):
    imdb = IMDb()
    search = imdb.search_movie(name)

    try:
        for res in search:
            if res.data['kind'] == 'movie':
                if int(year) + 1 >= int(res.data['year']) >= int(year) - 1:  # 通过预知电影年份进行匹配
                    return 'tt' + res.movieID
    except:
        print('没找到，使用其他方法继续查询......')
        return None


if __name__ == '__main__':
    getMVFromTMDB('200 Pounds Beauty', '2012')
