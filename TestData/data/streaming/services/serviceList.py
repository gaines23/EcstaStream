from tmdbv3api import TMDb
from tmdbv3api.tmdb import TMDb

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

class Provider(TMDb):
    _urls = {"movie_provider": "/watch/providers/movie", "tv_provider": "/watch/providers/tv"}

    def movie_provider(self, params):
        return self._get_obj(self._call(self._urls["movie_provider"], urlencode(params)), key="results")

    def tv_provider(self, params):
        return self._get_obj(self._call(self._urls["tv_provider"], urlencode(params)), key="results")


tmdb = TMDb()

tmdb.api_key = "2585280dc308165fb286c81bb4518b4b"
tmdb.debug = True

provider = Provider()
movies = provider.movie_provider({"language":"en-US", "watch_region":"US"})
shows = provider.tv_provider({"language":"en-US", "watch_region":"US"})


providerFile = open("data/streaming/services/services.json", "w", encoding='utf-8')

for m in movies:
    providerFile.write('{"display_priority":%d,"logo_path":"%s","provider_name":"%s","provider_id":%d}\n' %(m.display_priority, m.logo_path, m.provider_name, m.provider_id)) 

for s in shows:
    providerFile.write('{"display_priority":%d,"logo_path":"%s","provider_name":"%s","provider_id":%d}\n' %(s.display_priority, s.logo_path, s.provider_name, s.provider_id))

providerFile.close()


