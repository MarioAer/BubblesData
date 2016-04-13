# -*- coding: UTF-8 -*-
"""(forms.py) Flask-Login Example: Login Form"""
from flask_wtf import Form  # import from flask_wtf, NOT wtforms
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


# Define the LoginRorm class by sub-classing Form
class LoginForm(Form):
    # This form contains two fields with validators
    name = StringField(u'User Name:', validators=[InputRequired(), Length(max=20)])
    passwd = PasswordField(u'Password:', validators=[Length(min=4, max=16)])
