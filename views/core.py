# Imports
from __main__ import app
from models.models import db, Genre
from flask import render_template
import logging
from forms import *

# Seed genre table based on a static list
@app.before_first_request
def seed():
  try:
    genre_data = ('Alternative','Blues','Classical','Country','Electronic',
      'Folk','Funk','Hip-Hop ','Heavy Metal','Instrumental',
      'Jazz','Musical Theatre','Pop ','Punk','R&B','Reggae',
      'Rock n Roll ','Soul','Other')
    if Genre.query.get(1)==None:
      for genre in genre_data:
        genre_ = Genre(name=genre)
        db.session.add(genre_)
      db.session.commit()
      app.logger.setLevel(logging.INFO)
      app.logger.info("Initialized Genre Master data")
  except Exception as e:
    print(e)
    db.session.rollback()
  finally:
    db.session.close()

# Error handling for 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

# Error handling for 500
@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

# Main route
@app.route('/')
def index():
  return render_template('pages/home.html')