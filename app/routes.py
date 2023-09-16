from flask import Flask, render_template
from wtforms import SelectMultipleField
from app.forms import Majorform

def init_routes(app):

    @app.route('/', methods=['GET', 'POST'])
    def hello():
        return 'hello'

    @app.route('/major', methods=['GET', 'POST'])
    def SelectMajor():
        """
        Route handler for the index page.
        """

        form = Majorform()
        return render_template('form.html', form=form)