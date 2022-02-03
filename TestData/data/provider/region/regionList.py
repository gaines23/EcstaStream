from tmdbv3api import TMDb
from tmdbv3api.tmdb import TMDb

class Region(TMDb):
    _urls = {"watch_regions": "/watch/providers/regions"}

    def watch_regions(self):
        return self._get_obj(self._call(self._urls["watch_regions"], ""), key="results")

tmdb = TMDb()


tmdb.api_key = "2585280dc308165fb286c81bb4518b4b"
tmdb.debug = True

region = Region()

region = region.watch_regions()

regionFile = open("region.json", 'w', encoding='utf-8')
for r in region:
    regionFile.write('{"iso_3166_1":"%s","native_name":"%s"}\n' %(r.iso_3166_1, r.native_name))
regionFile.close()