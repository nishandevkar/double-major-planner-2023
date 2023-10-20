import sqlite3

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, make_response
from wtforms import SelectMultipleField
from app.forms import Majorform
from app.database import getCourses, getMajors, getUnits, process_units, process_duplicates, ifvalid, filter_non_core_units, organize_non_core_units
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
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

        # Ensure selected_majors is not None or empty
        if selected_majors:
            session['selected_majors'] = selected_majors
            rows,structures = getUnits(selected_majors)
            session['study_plan_data'] = rows
            session['study_plan_structures'] = structures
            response_data = {'redirect_url': '/studyPlan'}
        else:
            # Handle the case where selected_majors is None or empty
            # Maybe return an error message in the response or redirect to a different page
            response_data = {'error': 'No majors selected'}

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
        print(selected_majors)
        print(type(organized_non_core_units))  # This line will print the type of non_core_units
        print(organized_non_core_units)
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


    @app.route('/DownloadPDF', methods=['POST'])
    def download_pdf():
        plan = []
        data = request.json
        plan.clear()
        plan.extend(data.get('studyplan', []))
        response = make_response(generate_pdf(plan))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=study_plan.pdf'

        return response

    def generate_pdf(studyplan):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        for semester, courses in enumerate(studyplan, start=1):
            data = []
            data.append([f"Semester {semester}"])

            for course in courses:
                data.append([course])

            table = Table(data)


            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ])

            table.setStyle(style)
            elements.append(table)


        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()

        return pdf
