import click
import yaml
from .app import app, db
from .models import Anime, Song, Role, User, Status
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
    
    for role in ["Administrateur", "Modérateur", "Utilisateur"]:
        obj = Role(name = role)
        db.session.add(obj)

    db.session.commit()
    
    for status in ["Rejetée", "En attente", "Acceptée"]:
        obj = Status(name = status)
        db.session.add(obj)

    db.session.commit()
    
    if app.config['ENV'] != "production":
        
        from werkzeug.security import generate_password_hash
        
        admin_obj = User(
            username = "admin",
            email = "admin@admin.com",
            password = generate_password_hash("adminadmin"),
            role_id = 1
        )
        
        db.session.add(admin_obj)
        db.session.commit()
    
        
@app.cli.command()
def remove_db():
    '''Remove database/songs.db file'''
    if os.path.exists("website/database/songs.db"):
        os.remove("website/database/songs.db")
    else:
        print("The file does not exist")

