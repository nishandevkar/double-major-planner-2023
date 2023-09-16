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
