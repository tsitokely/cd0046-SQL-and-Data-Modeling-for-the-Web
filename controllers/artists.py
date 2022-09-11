# Imports
from models.models import Artist, City, artist_genre
from flask import render_template, request, flash, redirect, url_for
from forms import *
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#  Artists
#  ----------------------------------------------------------------

#  List all artists
def artists():
  # ✔: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

#  Search for artists
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  base_data = Artist.query.filter_by(id = artist_id).join(City).add_columns(City.city,City.state).first()

  if base_data is None:
    data={
    "id": artist_id,
    "name": "Artist Not Found",
    "genres": [],
    "city": "",
    "state": "",
    "phone": "",
    "website": "",
    "facebook_link": "",
    "seeking_venue": False,
    "seeking_description": "",
    "image_link": "",
    "past_shows": [{
      "venue_id": 0,
      "venue_name": "",
      "venue_image_link": "",
      "start_time": "1970-01-01"
    }],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0}
  else:
    data={
      "id": artist_id,
      "name": base_data[0].name,
      "genres": [],
      "city": base_data.city,
      "state": base_data.state,
      "phone": base_data[0].phone,
      "website": base_data[0].website,
      "facebook_link": base_data[0].facebook_link,
      "seeking_venue": base_data[0].seeking_venue,
      "seeking_description": base_data[0].seeking_description,
      "image_link": base_data[0].image_link,
      "past_shows": [{
        "venue_id": 0,
        "venue_name": "",
        "venue_image_link": "",
        "start_time": "1970-01-01"
      }],
      "upcoming_shows": [],
      "past_shows_count": 0,
      "upcoming_shows_count": 0,
    }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": artist_id,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  return redirect(url_for('show_artist', artist_id=artist_id))

#  Create Artist
#  ----------------------------------------------------------------

def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

def create_artist_submission():
  # called upon submitting the new artist listing form
  cityId = ''
  seekingVenueFormValue = False
  try:
    nameForm = request.form.get('name')
    cityForm = request.form.get('city')
    stateForm = request.form.get('state')
    search_city = City.query.filter(City.city.ilike("%"+cityForm+"%"), City.state.ilike("%"+stateForm+"%")).first()
    if search_city is None:
      newCity = City(city = cityForm, state = stateForm)
      db.session.add(newCity)
      db.session.flush()
      db.session.refresh(newCity)
      cityId = newCity.id
    else:
      cityId = search_city.id
    phoneForm = request.form.get('phone')
    imageLinkForm = request.form.get('image_link')
    fbLinkForm = request.form.get('facebook_link')
    websiteForm = request.form.get('website_link')
    seekingVenueForm = request.form.get('seeking_venue')
    if seekingVenueForm == 'y':
      seekingVenueFormValue = True
    seekingDescForm = request.form.get('seeking_description')
    artist = Artist(name = nameForm, city_id = cityId, phone = phoneForm, image_link = imageLinkForm, 
      facebook_link = fbLinkForm, website= websiteForm, seeking_venue = seekingVenueFormValue, seeking_description = seekingDescForm)
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
    print(e)
    db.session.rollback()
    # ✔: on unsuccessful db insert, flash an error instead.
    flash('An error occurred: Artist ' + request.form['name'] + ' could not be added!!!')
  finally:
    db.session.close()
  return render_template('pages/home.html')

# ------------------ Delete artist information -------------------------
#  Delete specific Artist based on a button
def delete_artist(artist_id):
  try:
    artist_to_delete = Artist.query.get(artist_id)
    local_object = db.session.merge(artist_to_delete)
    db.session.delete(local_object)
    db.session.commit()
    flash('Artist with name="' + artist_to_delete.name + '" was SUCCESSFULLY DELETED!')
  except Exception as e:
    print(e)
    db.session.rollback()
    flash('Artist with name="' + artist_to_delete.name + '" was NOT DELETED!')
  finally:
    db.session.close()
  return redirect(url_for('index'))