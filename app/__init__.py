from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes import init_routes
from app.database import builddb
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://root:8888@localhost/flaskdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '123456')
app.static_folder = 'static'
app.config.from_object(Config)
app.app_context().push()

db = SQLAlchemy(app)
builddb(db)

init_routes(app, db)
