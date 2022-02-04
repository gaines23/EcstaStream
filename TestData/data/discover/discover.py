from tmdbv3api import TMDb, Discover

tmdb = TMDb()

# Used to pull 10 movies + shows per streaming service (Top 10 Only)

tmdb.api_key = "2585280dc308165fb286c81bb4518b4b"
tmdb.debug = True

discover = Discover()


HBO = discover.discover_movies({"sort_by":"popularity.desc", "with_watch_providers": "HBO", "watch_region":"US"})

print(HBO)