from flask import Flask, render_template, request, jsonify
from wtforms import SelectMultipleField
from app.forms import Majorform

def init_routes(app):
    selected_majors = []

    @app.route('/')
    def hello():
        majors = ['Computer Science', 'Biology', 'History', 'Mathematics', 'Physics']
        return render_template('selectMajor.html', majors=majors)
        #return render_template('base.html')

    @app.route('/submit_majors', methods=['POST'])
    def SelectMajor():
        if request.method == 'POST':
            selected_majors = []
            data = request.json  # Assuming you are sending JSON data from the front-end

            # Example: Output selected majors to the console for testing
            selected_majors.clear()
            selected_majors.extend(data.get('selected_majors', []))
            print('Selected Majors:', selected_majors)
            # Respond with a success message
            response = {'message': 'Selected majors received successfully'}
            return jsonify(response)