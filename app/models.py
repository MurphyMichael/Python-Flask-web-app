from app import db

class User(db.Model):

    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    watchedlist = db.relationship('WatchedList', backref='owner', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    

#movie and show database class
class MovieShowDB(db.Model):

    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    yearReleased = db.Column(db.String(5), unique=True, nullable=False)
    genre = db.Column(db.String(25), unique=False, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)
    _type = db.Column(db.Boolean, unique=False, nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    

# watched list class connected by userID so it is just for that user, and movieID
class WatchedList(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movieID = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movieName = db.Column(db.String(50), nullable=False)
    movieGenre = db.Column(db.String(120), unique=False, nullable=False)