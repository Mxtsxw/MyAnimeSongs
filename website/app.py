from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
Bootstrap(app)