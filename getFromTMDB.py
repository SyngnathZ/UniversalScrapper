from tmdbv3api import TV

from imdb import IMDb
from tmdbv3api import TMDb
from tmdbv3api import Movie

tmdb = TMDb()
tmdb.api_key = 'YOUR API'
tmdb.language = 'zh'


def getMVFromTMDB(name, year):
    movie = Movie()
    search = movie.search(name)  # 输入电影名查询

    for res in search:
        try:
            if res.release_date != '':
                if int(year) + 1 >= int(res.release_date[:4]) >= int(
                        year) - 1:  # 通过预知电影年份进行匹配
                    print(res.title)
                    return res.title
        except:
            print('没找到，使用其他方法继续查询......')
            return None

    IMDBid = getMVFromIMDB(name, year)
    search = movie.external(IMDBid, 'imdb_id')  # 输入电影名查询
    return search.movie_results[0].title


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
