from flask import render_template, url_for, flash, redirect, request
import secrets
import os
from PIL import Image
from app import app, db, bcrypt, mail, moviesDF_top
from app.models import User, MovieDB, WatchedList
from app.forms import RegistrationForm, LoginForm, UpdateUserAccountForm, ResetForm, ResetPasswordForm, SearchForm
from flask_mail import Message
from flask_login import login_user, current_user, logout_user, login_required
from omdbapi.movie_search import GetMovie
import imdb



# route for the homepage
@app.route('/' , methods=['GET', 'POST'])
def Home():
    form = SearchForm()
    if form.validate_on_submit():
        search = SearchForm(request.form)
        if request.method == 'POST':
            return Results(search)
        

    return  render_template('home.html', form=form)

@app.route('/results/', methods=['GET', 'POST'])
def Results(search):
    searchStr = search.data['search']
    #userChoice = search.select.data['choices']

    if (len(searchStr) == 0):
        print(moviesDF_top)


   # moviesDF_top.style.format(make_clickable)
    return render_template('results.html', column_names=moviesDF_top.columns.values, row_data=list(moviesDF_top.values.tolist()), link_column="poster_path", zip=zip)
    

def path_to_image_html(posterLink):
    return '<img src="'+ posterLink + '" width="150" >'

@app.route('/movie', methods=['GET', 'POST'])
def movie():
    ia = imdb.IMDb() 

    movieName = request.args.get('title')

    search = ia.search_movie(movieName) 
    rand = ia.search_movie(movieName) 
    movieID = rand[0].movieID
    movie = ia.get_movie(movieID)
    moviePlot = movie['plot outline'] 
    movieRatings = movie['rating']
    movieGenre = movie['genres']
    poster = "http://img.omdbapi.com/?i=tt" + movieID + "&h=600&apikey=2dc44009"


    

    return render_template('movie.html', movieName=movieName, poster=poster, moviePlot = moviePlot, movieRatings = movieRatings, movieGenre = movieGenre)


# route that displays the register form
@app.route('/register', methods=['GET','POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = RegistrationForm()
    # if the form the user submitted is valid, then add them to the DB in the user table
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Go to Login to sign in to your account!', 'success')
        return redirect(url_for('Login'))
    return render_template('register.html', title='Register', form=form)


# route for the user login page
@app.route('/login', methods=['GET','POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = LoginForm()
    # if the the form submitted is valid, check to see if they exist by email, and check the password, if both are correct, log the user in.
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# route that logouts users when they click on "Logout", redirects to home
@app.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for('Home'))


# route for the user's account page
# This is a short profile page that only the user is able to see
# The user can change their email and username here, as well as their profile picture.
@app.route('/account', methods=['GET','POST'])
@login_required
def Account():
    form = UpdateUserAccountForm()
    if form.validate_on_submit():
        if form.userImage.data:
            profilePictureFile = saveUserPicture(form.userImage.data)
            current_user.profilePic = profilePictureFile
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('Account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for('static', filename='profilepics/'+ current_user.profilePic)
    return render_template('account.html', title='Account', image=image, form=form)


# route for the current user's watched list of movies. Will only show up if you are logged in.
@app.route('/watchedlist')
@login_required
def Watched_List():
   return render_template('watchedlist.html', title='Watched List')


# route to request password reset.
@app.route('/resetpassword', methods=['GET','POST'])
def ResetRequest():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = ResetForm()
    # if the email was found, a email will be sent with a password reset link
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        SendEmail(user)
        flash('Email sent with password reset instructions.', 'info')
        return redirect(url_for('Login'))
    return render_template('resetrequest.html', title='Reset Password', form=form)


# where the password resetting happens with the token.
@app.route('/resetpassword/<token>', methods=['GET','POST'])
def ResetRequestToken(token):
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    user = User.VerifyResetToken(token)
    if user is None:
        flash('Your reset token is invalid or has expired.', 'warning')
        return redirect(url_for('ResetRequest'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashedPassword
        db.session.commit()
        flash('Your password has been successfully changed!', 'success')
        return redirect(url_for('Login'))
    return render_template('resettoken.html', title='Reset Password', form=form)


# route to handle 404 errors and to send you back to home with a link
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404')

#         ###########functions to help in certain routes###########


# this function resized and saves pictures in the path app/static/profilepics.
def saveUserPicture(form_picture):
    random = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    fileName = random + f_ext
    picturePath = os.path.join(app.root_path, 'static/profilepics', fileName)
    outputSize = (125, 125)
    resize = Image.open(form_picture)
    resize.thumbnail(outputSize)
    resize.save(picturePath)

    return fileName

# the message that will be sent to the user if the email sent into the form is valid.
def SendEmail(user):
    token = user.GetResetToken()
    message = Message('Group4 Movie Database - Password Reset', sender='dontreply@grp4moviedb.com', recipients=[user.email])
    message.body = f''' Click on the link to reset your password!
{url_for('ResetRequestToken', token=token, _external=True)}

If you didn't request a password change, please ignore this message.
'''

    mail.send(message)