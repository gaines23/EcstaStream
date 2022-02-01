from tmdbv3api import TMDb, Genre
import json

tmdb = TMDb()

tmdb.api_key = "2585280dc308165fb286c81bb4518b4b"
tmdb.debug = True

genre = Genre()

movies = genre.movie_list()
shows = genre.tv_list()

genreFile = open("genre.json", 'w')
for m in movies:
    genreFile.write('{"id":%d,"name":"%s"}\n' %(m.id, m.name))

for s in shows:
    genreFile.write('{"id":%d,"name":"%s"}\n' %(s.id, s.name))
genreFile.close()