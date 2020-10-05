import pickle
import requests
from bs4 import BeautifulSoup

# URL - database source
url = 'https://reelgood.com/movies'

# get text request of given 'url'
html_content = requests.get(url).text
# Parse the html content using beautiful soup package
soup = BeautifulSoup(html_content, "lxml")

# Find assign table class and table rows
tableData = soup.find("table", attrs={"class": "css-1179hly"})
trs = tableData.find_all('tr')

#Loop through table rows.
# Search for table elemnt with appropriate HTML class name
movie_names = []
movie_ratings = []
for tr in trs:
    tds_names = tr.find_all('td', attrs={"class": "css-1u7zfla e126mwsw1"})
    tds_ratings  = tr.find_all('td', attrs={"class": "css-1u11l3y"})
    for td in tds_names:
        movie_names.append(td.text)
    for td in tds_ratings:
        movie_ratings.append(td.text)


# Group the 4 values of year and movie ratings together
#[year, viewing discretion(R rated), IMDB rating, Reel Good rating] -- 4 values that are grouped
def groupMovieAttr(list(attr))
	N = 4
	movie_ratings = [movie_ratings[n:n+N] for n in range(0, len(movie_ratings), N)]
groupMovieAttr(movie_ratings)

# Creating a dictionary of [key, value] = [movie names, list of movie attributes]
dict_movie = {}
for values, name  in zip(movie_ratings, movie_names):
    dict_movie[name] = values

# Pickle the movie dictionary
with open('movies.pickle', 'wb') as handle:
    pickle.dump(dict_movie, handle, protocol=pickle.HIGHEST_PROTOCOL)

'''
Pickled data Handling:
# load the pickled movie dictonaries
with open('movies.pickle', 'rb') as handle:
    b = pickle.load(handle)

print(dict_movie==b) # Check if the pickled data  is loaded successfully
'''





