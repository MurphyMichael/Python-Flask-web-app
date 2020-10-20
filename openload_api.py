import tmdbsimple as tmdb
tmdb.API_KEY = 'ae26a14563bbbd3ba76fa66d929c8f77'
search = tmdb.Search()
response = search.movie(query='Alien')
for s in search.results:
    try:
	    print("Title: ", s['title'], "\t ID: ", s['id'], "\t Release date: ", s['release_date'], "\t Popularity", s['popularity'])
    except:
        continue