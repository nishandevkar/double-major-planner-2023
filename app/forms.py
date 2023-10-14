from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField

class Majorform(FlaskForm):
    options = SelectMultipleField('Select options', choices=[
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4')
    ])