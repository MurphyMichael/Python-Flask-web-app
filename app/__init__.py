from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_login import LoginManager
from flask_mail import Mail
import imdb
import pandas as pd
import imdb.helpers
import dummyemail as secret
from IPython.display import HTML



app = Flask(__name__)

app.config['SECRET_KEY'] = 'aea103b9e51aee37e750b3e1ce0437ee'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

## various class calls from Flask classes for webapp functionality ##
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
movies = imdb.IMDb()
#assign "get top 250" function to variable search
search_top = movies.get_top250_movies()
#assing key:value to dict, moviesDF_top{'id': 'name'}
moviesDF_top = pd.DataFrame(columns = ['poster_path', 'title'])
poster_list = []
for name in search_top:
    ids = name.movieID
    posterLink = "http://img.omdbapi.com/?i=tt" + ids + "&h=600&apikey=2dc44009"
    moviesDF_top = moviesDF_top.append({'poster_path': str(posterLink), 'title': str(name)}, ignore_index=True)
moviesDF_top.style.set_properties(**{'text-align': 'center'}).hide_index()


# login manager for handling the current user logged in to handle multiple users.
loginManager = LoginManager(app)
loginManager.login_view = 'Login'
loginManager.login_message_category = 'info'

# this mail server is for users to be able to reset their passwords.
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = secret.USER
app.config['MAIL_PASSWORD']	= secret.PASS
mail = Mail(app)

from app import routes





# if the SQL database already exists, don't create another one.
if os.path.exists('site.db'):
    pass
else:
    db.create_all()