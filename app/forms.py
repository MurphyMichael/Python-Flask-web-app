from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

# form class for the registration
class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another username.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose another email.')

# form class for the login
class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateUserAccountForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    userImage = FileField('Change Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another username.')

    def validate_email(self, email):
        if email.data != current_user.email:    
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose another email.')

class ResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Password Reset')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('No account with that email. Please register first.')

class ResetPasswordForm(FlaskForm):

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')