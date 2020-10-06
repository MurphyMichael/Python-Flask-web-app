import sys
import pickle
import requests
from bs4 import BeautifulSoup

def movie_scraping_algorithm(link):
    # Get access to text with url request and parse Html content on webpage
    html_content = requests.get(link).text
    soup = BeautifulSoup(html_content, "lxml")

    # Find assign table class and table rows
    tableData = soup.find("table", attrs={"class": "css-1179hly"})
    trs = tableData.find_all('tr')

    # Loop through table rows.
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

    return movie_names, movie_ratings

# Group 4 values in movie attribute list
# Grouped Values -- [Year, View discretion, IMDB rating, Reelgood rating] 
def groupMovieAttr(attr):
    N = 4
    attr = [attr[n:n+N] for n in range(0, len(attr), N)]
    return attr
    
# Creating a dictionary of [key, value] = [movie names, list of movie attributes]
def create_dict(key, value):
    dict_movie = {}
    for name, values  in zip(key, value):
        dict_movie[name] = values
    return dict_movie

# Pickle the movie dictionary
def pickle_data(file):
    with open('movies.pickle', 'wb') as handle:
        pickle.dump(file, handle, protocol=pickle.HIGHEST_PROTOCOL)


def main(argv):
    if not sys.argv[0]:
        print("Error 404: File Not Found!")
        exit()

    # URL - database source
    url = 'https://reelgood.com/movies'

    movie_names, movie_ratings = movie_scraping_algorithm(url)      # Scrape Movie table data and return 2 lists
    movie_ratings = groupMovieAttr(movie_ratings)                   # Calling grouping move attributes function
    movie_dict = create_dict(movie_names, movie_ratings)            # Creating movie dictionary
    pickle_data(movie_dict)                                         # Pickle dictionary

    '''
    # Pickled data Handling:
    # load the pickled movie dictonaries
    with open('movies.pickle', 'rb') as handle:
        b = pickle.load(handle)

    print(movie_dict==b) # Check if the pickled data  is loaded successfully
    '''
    

if __name__ == "__main__":
    main(sys.argv)







