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
    conn = sqlite3.connect('./majors_database.db')
    cursor = conn.cursor()
    query = f"""
    SELECT major
    FROM MAJOR
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        majors.append(row[0])
    return majors

def getUnits(selected_majors):
    #units = [["all", "unit1", "unit2", "unit3"], [2, "unit4", "unit5", "unit6"], [3, "unit7", "unit8", "unit9", "unit10", "unit11"]]
    conn = sqlite3.connect('./new_commerce_final_with_students.db')
    cursor = conn.cursor()
    query = f"""
    SELECT unit.Code, unit.Title, major_with_level_group.level_group_name, major_with_level_group.major_name, unit.prerequisites, unit.Is_Core
    FROM unit, major_with_level_group
    WHERE
        (major_with_level_group.major_name='{selected_majors[0]}' OR major_with_level_group.major_name='{selected_majors[1]}') AND
        unit.Code=major_with_level_group.unit_code AND
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
    conn.close()
    return rows

def ifvalid(db, majors, units):
    flag = True
    ## TODO: Check if the units selection is valid.

    ##
    return flag

