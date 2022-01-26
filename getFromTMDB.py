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


def getTVFromTMDB(name):
    tv = TV()
    search = tv.search(name)  # 输入电影名查询

    if len(search) != 0:
        for res in search:
            return res.name, res.first_air_date[:4]
    else:
        return name, 'UNKONWN'  # 没搜到的情况

    # IMDBid = getMVFromIMDB(name, year)
    # search = movie.external(IMDBid, 'imdb_id')  # 输入电影名查询
    # try:
    #     result = search.movie_results[0].title
    #     return result
    # except:
    #     print(name, '没找到!!')
    #     return None


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
