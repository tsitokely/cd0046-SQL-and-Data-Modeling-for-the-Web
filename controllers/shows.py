# Imports
from models.models import Artist, Show, Venue, Artist
from flask import render_template, request, flash, redirect, url_for
from forms import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
#  Shows
#  ----------------------------------------------------------------

def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[]
  shows = Show.query.join(Venue).join(Artist).add_entity(Venue).add_entity(Artist).all()
  for show in shows:
    data.append({
    "venue_id": show[0].venue_id,
    "venue_name": show[1].name,
    "artist_id": show[2].id,
    "artist_name": show[2].name,
    "artist_image_link": show[2].image_link,
    "start_time": show[0].date.strftime("%m/%d/%Y")
    })
  return render_template('pages/shows.html', shows=data)

def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # ✔: insert form data as a new Show record in the db, instead
  try:
    artistIdForm = request.form.get('artist_id')
    venueIdForm = request.form.get('venue_id')
    startDateForm = request.form.get('start_time')
    show = Show(artist_id = artistIdForm, venue_id = venueIdForm, date = startDateForm)
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except Exception as e:
    print(e)
    db.session.rollback()
    # ✔: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. For more details: \r\n'+str(e))
  finally:
    db.session.close()
  return render_template('pages/home.html')