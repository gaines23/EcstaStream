from tmdbv3api import TMDb, Certification

tmdb = TMDb()

tmdb.api_key = "2585280dc308165fb286c81bb4518b4b"
tmdb.debug = True

cert = Certification()

movies = cert.movie_list().certifications
shows = cert.tv_list().certifications

certFile = open("data/certs/certs.json", "w", encoding='utf-8')

for us in movies["US"]:
    certFile.write('{"certification":"%s","meaning":"%s"}\n' %(us.certification, us.meaning))

for us in shows["US"]:
    certFile.write('{"certification":"%s","meaning":"%s"}\n' %(us.certification, us.meaning))

certFile.close()
