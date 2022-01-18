from tmdbv3api import TV
from tmdbv3api import TMDb
from tmdbv3api import Movie

tmdb = TMDb()
tmdb.api_key = 'YOUR_API_KEY'

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