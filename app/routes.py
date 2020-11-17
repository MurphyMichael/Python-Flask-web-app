from flask import render_template, url_for, flash, redirect
from app import app
from app.models import User, MovieShowDB, WatchedList
from app.forms import RegistrationForm, LoginForm

posts = [
    {
        'author' : 'Michael Murphy',
        'title' : 'Blog Post',
        'content' : 'First post content',
        'date_posted' : 'Today'
    }

]

@app.route('/')
def Home():
    return  render_template('home.html', posts=posts)


# def main():

@app.route('/register', methods=['GET','POST'])
def Register():	
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('Home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('Home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)