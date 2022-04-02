from flask.app import Flask
from website.models import *
from .app import app
from flask import request, jsonify


# The part corresponding to the API

# -- GET ALL ANIMES --
@app.route('/api/animes', methods=["GET"])
def get_animes_endpoint():
    # If limit is not defined, by default it is 15
    # If page is not defined, by default it is first page)
    
    try :
        page = int(request.args.get('page')) if request.args.get('page') is not None else 1
        limit = int(request.args.get('limit')) if request.args.get('limit') is not None else 15
    except ValueError:
        return "Invalid arguments", 400

    # Handling pagination
    animes = get_animes_pagination(page, limit)

    result = animes_schema.dump(animes.items)
    return jsonify(result)



# -- GET SPECIFIC ANIME --
@app.route('/api/anime/<id>', methods=["GET"])
def get_anime_endpoint(id):

    anime = Anime.query.get(id)
    return anime_schema.jsonify(anime)

# -- ADD ANIME -- 
@app.route('/api/animes', methods=["POST"])
def add_anime_endpoint():

    name = request.json["name"]
    img = request.json["img"]
    text = request.json["text"]

    new_anime = create_anime_from_api(name, img, text)

    return anime_schema.jsonify(new_anime)


# -- UPDATE ANIME --
@app.route('/api/anime/<id>', methods=["PUT"])
def put_anime_endpoint(id):

    anime = get_anime(id)

    aId = request.json["id"]
    name = request.json["name"]
    img = request.json["img"]
    text = request.json["text"]

    edit_anime_from_api(name, img, text, anime)

    db.session.commit()

    return anime_schema.jsonify(anime)

# -- DELETE ANIME --
@app.route('/api/anime/<id>', methods=["DELETE"])
def delete_anime_endpoint(id):

    anime = get_anime(id)

    db.session.delete(anime)
    db.session.commit()

    return anime_schema.jsonify(anime)

# -- GET ALL SONGS --
@app.route('/api/songs', methods=["GET"])
def get_songs_endpoint():

    username = request.args.get('username')

    all_songs = get_songs()
    result = songs_schema.dump(all_songs)

    return songs_schema.jsonify(result)

# -- GET SPECIFIC SONG --
@app.route('/api/song/<id>', methods=["GET"])
def get_song_endpoint(id):

    song = get_song(id)
    return song_schema.jsonify(song)




# Filtering

def filter(list, argument, sorted):
    if sorted:
        list.sort(key=lambda anime: anime.argument, reverse=True)
    else:
        list.sort(key=lambda anime: anime.argument)



# order = request.args.get('order')
#     filter_arg = request.args.get('filter')

#     if (order == "true"):
#         try:
#             filter(list, argument, True)