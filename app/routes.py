from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.models import User, MovieDB, WatchedList
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author' : 'Michael Murphy',
        'title' : 'Blog Post',
        'content' : 'First post content',
        'date_posted' : 'Today'
    }

]

# route for the homepage
@app.route('/')
def Home():
    return  render_template('home.html')


# route that displays the register form
@app.route('/register', methods=['GET','POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = RegistrationForm()
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
@app.route('/account')
@login_required
def Account():

    return render_template('account.html', title='Account')