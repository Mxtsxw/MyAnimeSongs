import click
import yaml
from .app import app, db
from .models import Anime, Song
import os.path

@app.cli.command()

def create_db():
    '''Create the tables and populates them with data.yml'''

    db.create_all()
    songs = yaml.load(open("website/database/data.yml"), Loader = yaml.SafeLoader)
    
    animes = dict()
    
    for song in songs:
        anime = song["anime"]
        if anime not in animes:
            obj = Anime(name = anime, img = song["img"])
            db.session.add(obj)
            animes[anime] = obj
    
    db.session.commit()
    
    for song in songs:
        anime = animes[song["anime"]]
        obj = Song(
            title = song["title"],
            relation = song["relation"],
            interpreter = song["interpreter"],
            ytb_url = song["ytb_url"],
            spoty_url = song["spoty_url"],
            anime_id = anime.id
        )
        
        db.session.add(obj)
    
    db.session.commit()
    
@app.cli.command()

def remove_db():
    '''Remove database/songs.db file'''
    if os.path.exists("website/database/songs.db"):
        os.remove("website/database/songs.db")
    else:
        print("The file does not exist")

