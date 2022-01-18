from tmdbv3api import TV
from tmdbv3api import TMDb
from tmdbv3api import Movie

tmdb = TMDb()
tmdb.api_key = '8a93c641a109bafadb38b526e7b2bb56'

tmdb.language = 'zh'

movie = Movie()
search = movie.search('疯狂麦克斯')

for res in search:
    print(res.title, '\n')


tv = TV()
show = tv.search('不完美的她')

for result in show:
    print(result.name)
    print(result.overview)