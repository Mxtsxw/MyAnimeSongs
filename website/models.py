from sqlalchemy.orm import backref
from .app import db

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    img = db.Column(db.String(200))
    
    def __repr__(self):
        return "<Anime (%d) %s>" % (self.id, self.name)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    relation = db.Column(db.String(10))
    interpreter = db.Column(db.String(200))
    ytb_url = db.Column(db.String(200))
    spoty_url = db.Column(db.String(200))
    anime_id = db.Column(db.Integer, db.ForeignKey("anime.id"))
    anime = db.relationship("Anime", backref = db.backref("songs", lazy = "dynamic"))

    def __repr__(self):
        return "<Song (%d) %s>" % (self.id, self.title)

def get_animes():
    return Anime.query.order_by('name').all()

def get_anime(id):
    return Anime.query.get_or_404(id)

def get_songs_anime(id):
    return Anime.query.get_or_404(id).songs.all()

def get_songs():
    return Song.query.order_by('title').all()

def get_song(id):
    return Song.query.get_or_404(id)

