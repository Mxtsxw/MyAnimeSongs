import click
import yaml
from .app import app, db
from .models import Anime, Song

@app.cli.command()
@click.argument('filename')

def create_db(filename):
    
    db.create_all()
    songs = yaml.load(open(filename), Loader = yaml.SafeLoader)
    
    animes = dict()
    
    for song in songs:
        anime = song["anime"]
        if anime not in animes:
            obj = Anime(name = anime)
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
    

