#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_sqlalchemy import SQLAlchemy
#----------------------------------------------------------------------------#
# Model Config.
#----------------------------------------------------------------------------#
db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

venue_genre = db.Table('Venue_Genre',
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    show = db.relationship('Show', backref='Venue', lazy=True)

    def __repr__(self):
      return f'<Venue: {self.id} {self.name}>'


artist_genre = db.Table('Artist_Genre',
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    show = db.relationship('Show', backref='Artist', lazy=True)

    def __repr__(self):
      return f'<Artist: {self.id} {self.name}>'

class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    artists = db.relationship('Artist', secondary=artist_genre,
      backref=db.backref('artist', lazy=True))
    venue = db.relationship('Venue', secondary=venue_genre,
      backref=db.backref('venue', lazy=True))

    def __repr__(self):
      return f'<Genre: {self.id} {self.name}>'

class Show(db.Model):
    __tablename__ = 'Show'

    date = db.Column(db.DateTime, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)

    def __repr__(self):
      return f'<Show: {self.venue_id} {self.artist_id}>'

class City(db.Model):
    __tablename__ = 'City'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    venue = db.relationship('Venue', backref='City', lazy=True)
    artist = db.relationship('Artist', backref='City', lazy=True)

    def __repr__(self):
      return f'<City: {self.id} {self.city} {self.state}>'

# ✔ Implement Show and Artist models, and complete all model relationships and properties, as a database migration.