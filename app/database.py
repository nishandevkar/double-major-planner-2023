import sqlite3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

def builddb(db):

    class Major(db.Model):
        __tablename__ = 'major'
        code = db.Column(db.String(16), primary_key=True)
        title = db.Column(db.String(64))
        undergraduateDegree = db.Column(db.String(16))
        school = db.Column(db.String(64))


    db.drop_all()
    db.create_all()

    db.session.add(Major(
        code='MJD-ACCTG',
        title='Accounting',
        undergraduateDegree='BCom',
        school='UWA Business School'
    ))
    db.session.commit()

def getCourses():
    courses = ['Commerce']
    return courses

def getMajors(courses):
    majors = []
    conn = sqlite3.connect('./commerce_database_solution1.sqlite')
    cursor = conn.cursor()
    query = f"""
    SELECT major_name
    FROM major_table
    WHERE major_name!='Foundation'
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        majors.append(row[0])
    return majors

def getUnits(selected_majors):
    #units = [["all", "unit1", "unit2", "unit3"], [2, "unit4", "unit5", "unit6"], [3, "unit7", "unit8", "unit9", "unit10", "unit11"]]
    conn = sqlite3.connect('./commerce_database_solution1.sqlite')
    cursor = conn.cursor()
    query = f"""
    SELECT unit_table.Code, unit_table.Title, unit_with_level.level_id, unit_with_major.major_name, unit_table.prerequisites, unit_table.Is_Core
    FROM unit_table, unit_with_major, unit_with_level
    WHERE
        (unit_with_major.major_name='{selected_majors[0]}' OR unit_with_major.major_name='{selected_majors[1]}' OR unit_with_major.major_name='Foundation') AND
        unit_table.Code=unit_with_major.Code AND unit_table.Code=unit_with_level.Code AND
        (Avail_1_Semester_Year IN ('1 Semester 2023', '2 Semester 2023') OR 
        Avail_2_Semester_Year IN ('1 Semester 2023', '2 Semester 2023') OR 
        Avail_3_Semester_Year IN ('1 Semester 2023', '2 Semester 2023') OR 
        Avail_4_Semester_Year IN ('1 Semester 2023', '2 Semester 2023') OR 
        Avail_5_Semester_Year IN ('1 Semester 2023', '2 Semester 2023') OR 
        Avail_6_Semester_Year IN ('1 Semester 2023', '2 Semester 2023') OR 
        Avail_7_Semester_Year IN ('1 Semester 2023', '2 Semester 2023'))
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    query = f"""
        SELECT *
        FROM major_table
        WHERE major_table.major_name='{selected_majors[0]}' OR major_table.major_name='{selected_majors[1]}'
        """
    cursor.execute(query)
    structures = cursor.fetchall()
    conn.close()
    return rows, structures

def ifvalid(db, majors, units):
    flag = True
    ## TODO: Check if the units selection is valid.

    ##
    return flag

