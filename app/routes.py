import sqlite3

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from wtforms import SelectMultipleField
from app.forms import Majorform
from app.database import getCourses, getMajors, getUnits, process_units, process_duplicates, ifvalid, filter_non_core_units, organize_non_core_units

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
        raw_data = session.get('study_plan_data')
        selected_majors = session.get('selected_majors')  
    
    # Process and organize core units
        processed_core_units = process_units(raw_data)
    
    # Process and organize non-core units
        non_core_units_raw = filter_non_core_units(raw_data)
        organized_non_core_units = organize_non_core_units(non_core_units_raw)

        print(organized_non_core_units)
    
    # Render the template with the organized data
        return render_template(
            'studyPlan.html', 
            units=processed_core_units,  # Corrected the variable name here
            non_core_units=organized_non_core_units,  # Passed the organized non-core units
            majors=selected_majors
        )

    @app.route('/ifValid', methods=['POST'])
    def ifValid():
        data = request.json
        selected_majors = data.get('selected_majors','')
        selected_units = data.get('selected_units','')
        response = {'ifvalid': ifvalid(selected_majors, selected_units)}
        return jsonify(response)


