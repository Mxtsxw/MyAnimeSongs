from flask.app import Flask
from website.models import *
from .app import app, mkpath
import os.path
from flask import request, jsonify, send_file


# The part corresponding to the API

# -- GET ALL ANIMES --
@app.route('/api/animes', methods=["GET"])
def get_animes_endpoint():
    # If limit is not defined, by default it is 15
    # If page is not defined, by default it is first page)
    
    try :
        tag = request.args.get("tag") if request.args.get("tag") is not None else ""
        page = int(request.args.get('page')) if request.args.get('page') is not None else 1
        limit = int(request.args.get('limit')) if request.args.get('limit') is not None else 15
    except ValueError:
        tag = ""
        page = 1
        limit = 15

    # Handling pagination & filters
    animes = get_anime_by_filter(tag, page, limit).items

    # Handling Anime sorting
    order = request.args.get('order')
    argument = request.args.get('argument') if request.args.get('argument') is not None else "id"
    
    if order == "desc":
        sort_animes(animes, argument, True)
    else: 
        sort_animes(animes, argument, False)

    result = animes_schema.dump(animes)
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

    try :
        tag = request.args.get("tag") if request.args.get("tag") is not None else ""
        page = int(request.args.get('page')) if request.args.get('page') is not None else 1
        limit = int(request.args.get('limit')) if request.args.get('limit') is not None else 15
    except ValueError:
        tag = ""
        page = 1
        limit = 15

    # Handling pagination & filters
    songs = get_song_by_filter(tag, page, limit).items
    songs.extend(Song.query.filter(Song.interpreter.like(f'%{tag}%')).paginate(page,limit).items)
    songs = list(dict.fromkeys(songs))
    # songs.extend(Song.query.filter(Song.anime.name.like(f'%{tag}%')).paginate(page, limit).items)

    # Handling Songs sorting
    order = request.args.get('order')
    argument = request.args.get('argument') if request.args.get('argument') is not None else "id"
    
    if order == "desc":
        sort_songs(songs, argument, True)
    else: 
        sort_songs(songs, argument, False)

    result = songs_schema.dump(songs)

    return songs_schema.jsonify(result)

# -- GET SPECIFIC SONG --
@app.route('/api/song/<id>', methods=["GET"])
def get_song_endpoint(id):

    song = get_song(id)
    return song_schema.jsonify(song)

# -- UPDATE SONG --
@app.route('/api/song/<id>', methods=["PUT"])
def put_song_endpoint(id):

    song = get_song(id)

    title = request.json["title"]
    interpreter = request.json["interpreter"]
    relation = request.json["relation"]
    youtube = request.json["img"]
    spotify = request.json["text"]

    edit_song(title, interpreter, relation, youtube, spotify, song)

    db.session.commit()

    return song_schema.jsonify(song)

# -- DELETE SONG --
@app.route('/api/song/<id>', methods=["DELETE"])
def delete_song_endpoint(id):

    song = get_song(id)

    db.session.delete(song)
    db.session.commit()

    return song_schema.jsonify(song)


# Sorting Animes
def sort_animes(animes, argument, ordered):
    if argument == "title":
        animes.sort(key=lambda anime: anime.name, reverse=ordered)
    else:
        animes.sort(key=lambda anime: anime.id, reverse=ordered)

# Sorting Songs
def sort_songs(songs, argument, ordered):
    if argument == "title":
        songs.sort(key=lambda song: song.title, reverse=ordered)
    elif argument == "interpreter":
        songs.sort(key=lambda song: song.interpreter, reverse=ordered)
    elif argument == "relation":
        songs.sort(key=lambda song: (song.relation, song.title), reverse=ordered)
    elif argument == "anime":
        songs.sort(key=lambda song: (song.anime_id, song.relation, song.title), reverse=ordered)
    else:
        songs.sort(key=lambda song: song.id, reverse=ordered)


@app.route('/api/image/<name>')
def get_image_endpoint(name):
    filename = os.path.join(os.path.dirname(__file__)) + f"\static\images\{name}"
    try:
        return send_file(filename, mimetype='image/jpeg')
    except FileNotFoundError:
        return "File not found", 404