# Imports
from inspect import trace
from models.models import Artist, City, artist_genre
from flask import render_template, request, flash, redirect, url_for
from forms import *
from flask_sqlalchemy import SQLAlchemy
import traceback

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
  # ✔: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # TODO: num_upcoming show
  search_term=request.form.get('search_term', '')
  search_data = Artist.query.filter(Artist.name.ilike("%"+search_term+"%")).all()
  datastore = []
  for data in search_data:
    datastore.append({
    "id": data.id,
    "name": data.name,
    "num_upcoming_shows": 0,
    })
  response={
    "count": len(search_data),
    "data": datastore
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # ✔: replace with real artist data from the artist table, using artist_id
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
  # TODO: genre
  search_data = Artist.query.filter_by(id = artist_id).join(City).add_columns(City.city,City.state).first()
  form = ArtistForm()
  artist={
    "id": artist_id,
    "name": search_data[0].name,
    "genres": [],
    "city": search_data.city,
    "state": search_data.state,
    "phone": search_data[0].phone,
    "website": search_data[0].website,
    "facebook_link": search_data[0].facebook_link,
    "seeking_venue": search_data[0].seeking_venue,
    "seeking_description": search_data[0].seeking_description,
    "image_link": search_data[0].image_link
  }
  # ✔: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

def edit_artist_submission(artist_id):
  # ✔: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  existing_artist = Artist.query.filter_by(id = artist_id).join(City).add_columns(City.id, City.city,City.state).first()
  all_city = City.query.all()
  seekingVenueValue = False
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  print(existing_artist)
  try:
    nameForm = request.form.get('name')
    addressForm = request.form.get('address')
    cityForm = request.form.get('city')
    print(existing_artist.city)
    stateForm = request.form.get('state')
    phoneForm = request.form.get('phone')
    imageLinkForm = request.form.get('image_link')
    fbLinkForm = request.form.get('facebook_link')
    websiteForm = request.form.get('website_link')
    seekingVenueForm = request.form.get('seeking_venue')
    if seekingVenueForm == 'y':
      seekingVenueValue = True
    seekingDescForm = request.form.get('seeking_description')
    if (existing_artist.city != cityForm) or (existing_artist.state != stateForm):
      if cityForm not in all_city[0].city or stateForm not in all_city[0].state:
        new=City(city=cityForm,state=stateForm)
        db.session.add(new)
        db.session.commit
        x=new
        print(x)
    existing_artist[0].name = nameForm
    existing_artist[0].address = addressForm
    existing_artist[0].phone = phoneForm
    existing_artist[0].image_link = imageLinkForm
    existing_artist[0].facebook_link = fbLinkForm
    existing_artist[0].website_link = websiteForm
    existing_artist[0].seeking_venue = seekingVenueValue
    existing_artist[0].seeking_description = seekingDescForm
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully Updated!')
  except Exception as e:
    traceback.print_exc()
    db.session.rollback()
    # ✔: on unsuccessful db insert, flash an error instead.
    flash('An error occurred: Artist ' + request.form['name'] + ' could not be Updated!!!')
  finally:
    db.session.close()
  return redirect(url_for('artists_bp.show_artist', artist_id=artist_id))

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