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
def get_anime_route(id):

    anime = Anime.query.get(id)
    return anime_schema.jsonify(anime)

# -- ADD ANIME -- 
@app.route('/api/animes', methods=["POST"])
def add_anime_route():

    name = request.json["name"]
    img = request.json["img"]
    text = request.json["text"]

    new_anime = create_anime_from_api(name, img, text)
    print(new_anime)

    return anime_schema.jsonify(new_anime)


# -- UPDATE ANIME --
@app.route('/api/anime/<id>', methods=["PUT"])
def put_anime_route(id):

    anime = get_anime(id)

    aId = request.json["id"]
    name = request.json["name"]
    img = request.json["img"]
    text = request.json["text"]

    edit_anime_from_api(name, img, text, anime)

    db.session.commit()

    return anime_schema.jsonify(anime)

# -- GET ALL SONGS --
@app.route('/api/songs', methods=["GET"])
def get_songs_route():
    all_songs = get_songs()
    result = songs_schema.dump(all_songs)

    return songs_schema.jsonify(result)