from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import pickle

app = Flask(__name__)

# change to name of your database; add path if necessary
db_name = 'sockmarket.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

#User database class
class UserDB(db.Model):

    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, )
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), unique=True, nullable=False)
    firstName = db.Column(db.String(50), unique=False, nullable=False)
    lastName = db.Column(db.String(50), unique=False, nullable=False)
    #watchedList

    def __init__(self, username, password, firstName, lastName):
        
        self.username = username
        self.password = password
        self.firstName = firstName
        self.lastName = lastName

#movie and show database class
class MovieShowDB(db.Model):

    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True, )
    title = db.Column(db.String(80), nullable=False, unique=True)
    yearReleased = db.Column(db.String(5), unique=True, nullable=False)
    genre = db.Column(db.String(25), unique=False, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)
    _type = db.Column(db.Boolean, unique=False, nullable=False)

    def __init__(self, title, yearReleased, genre, description, _type):
        
        self.title = title
        self.yearReleased = yearReleased
        self.genre = genre
        self.description = description
        self._type = _type

# watched list class connected by userID so it is just for that user, and movieID
class WatchedList(db.Model):

    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movieID = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movieName = db.Column(db.String(50), nullable=False)

    def __init__(self, userID, movieID, movieName):

        self.userID = userID
        self.movieID = movieID
        self.movieName = movieName

# NOTHING BELOW THIS LINE NEEDS TO CHANGE
# this route will test the database connection and nothing more
@app.route('/')
def testdb():
    try:
        db.session.query('1').from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
# def main():
	

if __name__ == '__main__':

    app.run(debug=True)