from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os.path
from flask_login import LoginManager
import imdb
import pandas as pd
import imdb.helpers

# no changes

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aea103b9e51aee37e750b3e1ce0437ee'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# various class calls from Flask classes for webapp functionality
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = 'Login'
loginManager.login_message_category = 'info'
from app import routes

movies = imdb.IMDb()

#assign "get top 250" function to variable search
search_top = movies.get_top250_movies()

#assing key:value to dict, moviesDF_top{'id': 'name'}
moviesDF_top = pd.DataFrame(columns = ['id', 'title'])
for name in search_top:
	ids = name.movieID
	moviesDF_top = moviesDF_top.append({'id' : ids, 'title': str(name) }, ignore_index=True)
"""
poster_list = []
for name in search_top:
	ids = name.movieID 
	movieAccess = movies.get_movie(ids)
	poster_list += movieAccess.data['cover url']
moviesDF_top['poster_path'] = poster_list
print(moviesDF_top['poster_path'])
"""
"""
posterDF = pd.DataFrame(columns = ['poster_path'])
for name in search_top:
	m = movies.get_movie(name.movieID) # Avatar.
	posterDF = posterDF.append({'poster_path': imdb.helpers.fullSizeCoverURL(m)}, ignore_index=True)
"""
# if the SQL database already exists, don't create another one.
if os.path.exists('site.db'):
    pass
else:
    db.create_all()