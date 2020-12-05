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


app = Flask(__name__)

app.config['SECRET_KEY'] = 'aea103b9e51aee37e750b3e1ce0437ee'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

## various class calls from Flask classes for webapp functionality ##
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

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