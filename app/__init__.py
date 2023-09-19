from flask import Flask, render_template
from app.routes import init_routes
from app.database import builddb
from flask_sqlalchemy import SQLAlchemy

class Config:
    """
    database username:root
    password:123456
    database name:flaskdb
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/flaskdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)

app.config['SECRET_KEY'] = '123456'

app.static_folder = 'static'
app.config.from_object(Config)
app.app_context().push()

db = SQLAlchemy(app)
builddb(db)


init_routes(app, db)
