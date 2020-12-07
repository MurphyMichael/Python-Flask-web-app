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

#read excel file into a df object, 'data'
data = pd.read_excel(r"app/IMDB_Top250.xls") 
data = data.dropna()  #clean dataset of null values

#initialize another df to avoid redundancy and overwriting
moviesDF_top = pd.DataFrame()
poster_list = []

#access OMDB api to assign move poster links to df
for i, row in data.iterrows():
    m_id = row["imdbID"]
    #movie ID manually inserted into API call to access Movie poster
    posterLink = "http://img.omdbapi.com/?i=" + m_id + "&h=600&apikey=2dc44009"
    data.at[i, 'poster_path'] = posterLink

#Assigning cleaned df to a copy
data.rename(columns={"imdbID":"ids", "Title":"title", "Year":"year", "Genre":"genres"}, inplace = True)
moviesDF_top = data.copy()



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