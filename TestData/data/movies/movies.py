from tmdbv3api import TMDb, Movie
import json

tmdb = TMDb()

tmdb.api_key = "2585280dc308165fb286c81bb4518b4b"
tmdb.debug = True

movie = Movie()
testid = 2502


md = movie.details(testid)

# me = movie.external_ids(testid)
mi = movie.images(testid)
# mv = movie.videos(testid)
#mvp = movie.watch_providers(testid)
# mc = movie.credits(testid)

# movieFile = open("movie.json", 'w', encoding='utf-8')
# for m in md:
#     movieFile.write('{"display_priority":%d,"logo_path":"%s","provider_name":"%s","provider_id":%d}\n' %(m.display_priority, m.logo_path, m.provider_name, m.provider_id))

# for mv in mvp:
#     movieFile.write('{"}')
# movieFile.close()


print(mi)