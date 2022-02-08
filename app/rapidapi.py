#import os
#import environ
#import requests
#from tmdbv3api import TMDb, Movie

#env = environ.Env()
#environ.Env.read_env()

#tmdb_key = env('TMDB_API_KEY')
#tmdb = TMDb()
#tmdb.tmdb_key = tmdb_key

#movie = Movie()
#movieid = 2502
#details = movie.details(movieid)
#imdbid = details.imdb_id

#class ImdbRapiApi(object):
#    #imdbID = "tt0372183"
#    url = "https://movie-database-imdb-alternative.p.rapidapi.com/"
#    querystring = {"i":{imdbid},"type":"movie","r":"json"}

#    Imdb_URL = "movie-database-imdb-alternative.p.rapidapi.com"
#    URL_API = "93f4b600aemshd9c2d876469f714p1c0cb3jsn18656827b06a"

#    headers = {
#        'x-rapidapi-host': Imdb_URL,
#        'x-rapidapi-key': URL_API
#        }

#    response = requests.request("GET", url, headers=headers, params=querystring)

