from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(),  EqualTo('confirm', message='Passwords must match')]) #se podria agregar lo de repetir la contraseña
    confirm = PasswordField ('Repeat Password')
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign up!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) 
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in!')

class ContractForm(FlaskForm): #creo formulario de contrato
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description')
    price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Create contract')
    buy = SubmitField('Buy')


class WalletForm(FlaskForm): #formulario de billetera
    name = StringField('Title', validators=[DataRequired(), Length(max=128)])
    key = TextAreaField('Key', validators =[DataRequired()])
    submit = SubmitField('Connect wallet')
