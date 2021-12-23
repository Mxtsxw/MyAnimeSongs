from flask.app import Flask
from wtforms.fields.simple import HiddenField
from .app import app
from flask import render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from website.models import get_anime, get_animes, get_song, get_songs, get_songs_anime

@app.route("/")
def home():
    return render_template(
        "index.html",
        title="My Anime Songs"
    )

class AnimeRequest(FlaskForm):
    anime = StringField("nom", validators = [DataRequired()])
    

@app.route("/request/")
def request_song():
    form = AnimeRequest()
    return render_template(
        "anime-request.html",
        form = form,
        animes = get_animes()
    )