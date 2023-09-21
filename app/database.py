from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

def getCourses(db):
    courses = ['commerce']
    return courses

def getMajors(db, courses):
    majors = ['Computer Science', 'Biology', 'History', 'Mathematics', 'Physics']
    return majors

def getUnits(db, major):
    units = [["all", "unit1", "unit2", "unit3"], [2, "unit4", "unit5", "unit6"], [3, "unit7", "unit8", "unit9", "unit10", "unit11"]]
    return units

def ifvalid(db, majors, units):
    flag = True
    ## TODO: Check if the units selection is valid.

    ##
    return flag