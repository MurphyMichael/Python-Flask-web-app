
import numpy
import json
import random
import pickle
import os
import pathlib
import nltk
import pandas as pd 
import ast
import re
import string
from tabulate import tabulate


def main():
    print =("!!!!! IN MAIN !!!!!!")

    # call read_CSV function, to get pandas df's
    # raw df returned for metadata and keywords
    metadata_df = read_CSV()
    metadata_df= cleanDF(metadata_df)
    #metadata_df.to_csv('metadata_prep.csv')


    response = ""
    username_dict = CheckForUserPickle() 
    curr_username = Welcome(response)
    

   

    inp = input("Enter genres separated by spaces that you like")
    
    filtered_df = searchAlgo(inp, meta_df)
    sort_filter_df(filtered_df)
 
    
     

    """
    """

    with open('person_dictionary.pkl', 'wb') as f:
        pickle.dump(username_dict, f)

#------------------------------------------------------------------------------------------------------------------------------------------*******************


def read_CSV():
    file_metadata = os.path.join(os.getcwd(), "movies_metadata.csv")
    #if not file_metadata.exists() :
    #   print("Error 404!! CSV metadata not found")
    #    exit(0)
        
    df1 = pd.read_csv(file_metadata, low_memory=False)
    df1 = df1.astype(str)
    df1_metadata = df1.apply(lambda x: x.astype(str).str.lower())

    return df1_metadata
    #print(df1_metadata[:1][1:])
    #print(df2_keywords[:1][1:])
def cleanDF(meta):
    meta = meta.drop(['belongs_to_collection','homepage','revenue','status'],axis=1)
    meta = meta.drop(['original_language','production_countries','production_companies','spoken_languages','video'],axis=1)
    meta = meta.dropna(subset=['imdb_id','poster_path'])
    
    meta['genres'] = meta['genres'].apply(lambda x: ast.literal_eval(x))
    meta['genres'] = meta['genres'].apply(lambda x: ', '.join([d['name'] for d in x]))
    #print(meta['genres'].unique())

    meta['imdbURL'] = 'https://www.imdb.com/title/' + meta['imdb_id'] + '/'
    meta['tmdbURL'] = 'https://www.themoviedb.org/movie/' + meta['id']
    meta['ImageURL'] = 'https://image.tmdb.org/t/p/w92' + meta['poster_path']

    return meta

def CheckForUserPickle():
    path = pathlib.Path("person_dictionary.pkl")
    isFile = os.path.isfile(path)
    if(isFile):
        person_dict = pickle.load(input_file)
    else:
        person_dict = []

    return person_dict

def Welcome(response):
    print("\n")
    print("Let's set a profile for you before we start...\n")
    print("...\n")
    response = input("What is your name? ")
    return response

def searchAlgo(genre, meta):
    movie_object_response = []
    genre_list = genreList(meta)
    genre = cleanUserResponse(genre)
    """
    user_genre = []
    for word in genre:
        user_genre.append(word) 
    print(user_genre)
    """
    #print(genre)
    #print(genre_list)

    for word in genre_list:
        if word not in genre_list:
            print("Your response was not a defined Genre!")
            continue
    regstr = '|'.join(genre)
    
    print(meta['genres'].dtypes)
    
    #df2 = [col for col in meta.genres if regstr in col]
    filter1 = meta["genres"].isin(genre) 
    #filter2 = data["genres"].isin(["Engineering", "Distribution", "Finance" ])
    #df2 = meta[filter1]
    
    meta['bool'] = meta['genres'].str.contains('|'.join(genre))
    df_filter = meta[meta['bool'] == True]
    
    #df2 = meta['genres'].str.lower().str.contains(genre)

    #print(df2['genres'])
    #print(genre_list)
    return df_filter

def sort_filter_df(filter_df):
    sort_df = filter_df.sort_values('popularity', ascending=False)
    sort_df = filter_df[['original_title', 'genres','release_date', 'runtime']]
    #print(sort_df.head())
    sorted_df = sort_df.head(10)
    print(tabulate(sorted_df, headers = 'keys', tablefmt = 'psql'))
    

#-----------------------------------
def cleanUserResponse(genre):
    genre = genre.lower()
    genre = nltk.word_tokenize(genre)
    genre = [''.join(c for c in s if c not in string.punctuation) for s in genre]
    for word in genre:
        if not word:
            genre.remove(word)

    return genre

def genreList(meta):
    unique = meta["genres"].unique()
    

    genre_list = []
    listOfGenre = []
    for sent in unique:
        sent = sent.split()
        for word in sent:
            genre_list.append(word.lower())
    genre_list = list(dict.fromkeys(genre_list))
    for word in genre_list:
        word = re.sub(r'[,:;\d]', '',word)
        listOfGenre.append(word)
    
    return listOfGenre

if __name__ == "__main__":
    print("!!!! IN ____MAIN____!!!!!")
    main()