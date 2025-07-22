from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class VerifyForm(FlaskForm):
    digit1 = StringField('Digit 1', validators=[InputRequired(), Length(min=1, max=1)])
    digit2 = StringField('Digit 2', validators=[InputRequired(), Length(min=1, max=1)])
    digit3 = StringField('Digit 3', validators=[InputRequired(), Length(min=1, max=1)])
    digit4 = StringField('Digit 4', validators=[InputRequired(), Length(min=1, max=1)])