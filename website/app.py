from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
import os.path

app = Flask(__name__)
Bootstrap(app)

def mkpath(path):
    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), path)
    )

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///'+mkpath('database/songs.db')
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)