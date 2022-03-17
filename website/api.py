from flask.app import Flask
from website.models import *
from .app import app
from flask import request, jsonify


# The part corresponding to the API

# -- GET ALL ANIMES --
@app.route('/api/animes', methods=["GET"])
def get_animes():
    all_animes = Anime.query.all()
    result = animes_schema.dump(all_animes)
    return jsonify(result)


# -- GET SPECIFIC ANIME --
@app.route('/api/anime/<id>', methods=["GET"])
def get_anime(id):

    anime = Anime.query.get(id)
    return anime_schema.jsonify(anime)

# -- ADD ANIME -- 
@app.route('/api/animes', methods=["POST"])
def add_anime():

    name = request.json["name"]
    img = request.json["img"]
    text = request.json["text"]

    new_anime = create_anime_from_api(name, img, text)
    print(new_anime)

    return anime_schema.jsonify(new_anime)


# -- UPDATE ANIME --

