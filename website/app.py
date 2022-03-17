from flask import Flask
from flask_bootstrap5 import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
import os.path
from flask_login import LoginManager, login_manager
from flask_cors import CORS

app = Flask(__name__)
Bootstrap(app)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

def mkpath(path):
    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), path)
    )

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///'+mkpath('database/songs.db')
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

app.config['SECRET_KEY'] = '328396918c21bf73e52e9b867c7a2dcb88a083e200022e7380bc280e3017a617'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'