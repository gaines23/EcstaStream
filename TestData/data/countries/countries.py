from tmdbv3api import TMDb, Configuration

tmdb = TMDb()
tmdb.api_key = "2585280dc308165fb286c81bb4518b4b"
tmdb.debug = True

configuration = Configuration()
countries = configuration.countries()

countryFile = open("data/countries/countries.json", "w", encoding='utf-8')

for c in countries:
    countryFile.write('{"iso_3166_1":"%s","english_name":"%s"}\n' %(c.iso_3166_1, c.english_name))
countryFile.close()