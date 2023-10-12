import sqlite3
from app.database import filter_non_core_units
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from wtforms import SelectMultipleField
from app.forms import Majorform
from app.database import getCourses, getMajors, getUnits, process_units, process_duplicates, ifvalid

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

        # 将选择的专业保存到 session
        session['selected_majors'] = selected_majors

        #其他代码...
        rows, structures = getUnits(selected_majors)
        session['study_plan_data'] = rows
        session['study_plan_structures'] = structures

        response_data = {'redirect_url': '/studyPlan'}
        return jsonify(response_data)

    
    
    @app.route('/result')
    def result():
        raw_data = session.get('study_plan_data')  # 获取 session 中的原始数据
        selected_majors = session.get('selected_majors', [])  # 从 session 中获取专业
    
         # 使用 filter_non_core_units 函数过滤非核心单元
        non_core_units = filter_non_core_units(raw_data)
    
        # 将非核心单元和已选专业作为变量传递给 result.html 模板
        return render_template('result.html', majors=selected_majors, units=non_core_units)






    @app.route('/studyPlan', methods=['GET'])
    def studyPlan():
        raw_data = session.get('study_plan_data')
        #print(f"Raw Data: {raw_data}")  # print raw data
        processed_data = process_units(raw_data)
        return render_template('studyPlan.html', units=processed_data)


    @app.route('/ifValid', methods=['POST'])
    def ifValid():
        data = request.json
        selected_majors = data.get('selected_majors','')
        selected_units = data.get('selected_units','')
        response = {'ifvalid': ifvalid(selected_majors, selected_units)}
        return jsonify(response)


