from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from wtforms import SelectMultipleField
from app.forms import Majorform
from app.database import getCourses, getMajors

def init_routes(app, db):

    @app.route('/')
    def index():
        return redirect('/selectCourses')

    @app.route('/selectCourses')
    def selectCourses():
        courses = getCourses(db)
        return render_template('selectCourse.html', courses=courses)
        # return render_template('base.html')
    @app.route('/submit_course', methods=['POST'])
    def submitCourse():
        data = request.json
        selected_course = data.get('selected_course','')
        majors = getMajors(db, selected_course)
        print(majors)
        session['majors'] = majors
        response = {'majors': majors}
        return jsonify(response)

    @app.route('/selectMajor', methods=['GET','POST'])
    def selectMajor():
        majors = session.get('majors', [])  # 从session中获取专业数据
        print(majors)
        return render_template('selectMajor.html', majors=majors)
        #return render_template('base.html')

    @app.route('/submit_majors', methods=['POST'])
    def submitMajors():
        if request.method == 'POST':
            selected_majors = []
            data = request.json

            selected_majors.clear()
            selected_majors.extend(data.get('selected_majors', []))
            print('Selected Majors:', selected_majors)
            # Respond with a success message
            response = {'message': 'Selected majors received successfully'}
            return jsonify(response)