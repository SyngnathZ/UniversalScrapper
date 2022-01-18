from tmdbv3api import TV
from tmdbv3api import TMDb
from tmdbv3api import Movie

tmdb = TMDb()
tmdb.api_key = 'YOUR TOKEN'
tmdb.language = 'zh'


def getMVFromTMDB(name, year):
    movie = Movie()
    search = movie.search(name)  # 输入电影名查询

    for res in search:
        try:
            if res.release_date[:4] == year:  # 通过预知电影年份进行匹配
                print(res.title)
                break
        except:
            print('没找到，使用其他方法继续查询......')
