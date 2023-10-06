import sqlite3

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from wtforms import SelectMultipleField
from app.forms import Majorform
from app.database import getCourses, getMajors, getUnits

def init_routes(app):

    @app.route('/')
    def index():
        return redirect('/selectCourses')
    
    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/selectCourses')
    def selectCourses():
        courses = getCourses()
        return render_template('selectCourse.html', active_page='selectCourses', courses=courses)
        # return render_template('base.html')
    @app.route('/submit_course', methods=['POST'])
    def submitCourse():
        data = request.json
        selected_course = data.get('selected_course','')
        majors = getMajors(selected_course)
        # print(majors)
        session['majors'] = majors
        response = {'majors': majors}
        return jsonify(response)

    @app.route('/selectMajor', methods=['GET','POST'])
    def selectMajor():
        majors = session.get('majors', [])  # 从session中获取专业数据
        # print(majors)
        return render_template('selectMajor.html', active_page='selectMajor', majors=majors)
        #return render_template('base.html')

    @app.route('/submit_majors', methods=['GET', 'POST'])
    def submitMajors():

        selected_majors = []
        data = request.json

        selected_majors.clear()
        selected_majors.extend(data.get('selected_majors', []))
        # print('Selected Majors:', selected_majors)
        # Respond with a success message
        # response = {'message': 'Selected majors received successfully'}
        # return jsonify(response)
        rows,structures = getUnits(selected_majors)
        session['study_plan_data'] = rows
        session['study_plan_structures'] = structures
        # print(rows)
        # return redirect(url_for('studyPlan'))
        response_data = {'redirect_url': '/studyPlan'}
        return jsonify(response_data)


    @app.route('/studyPlan', methods=['GET'])
    def studyPlan():
        study_plan_data = session.get('study_plan_data')
        # print(session.get('study_plan_data'))
        # print(session.get('study_plan_structures'))
        return render_template('studyPlan.html', active_page='studyPlan')


