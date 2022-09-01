# Imports
from __main__ import app
from models.models import db, Genre, Venue, City, venue_genre
from flask import render_template, request, flash, redirect, url_for
from forms import *

# ------------------ Get venues information -------------------------
#  List all venues
@app.route('/venues')
def venues():
  # TODO: num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  venue_per_city = []
  venue_base_data = Venue.query.all()
  city_data = City.query.all()
  # TODO: add upcoming show
  for city in city_data:
    for venue in venue_base_data:
      if city.id == venue.city_id:
        venue_per_city.append({
          "id": venue.id,
          "name": venue.name, 
          "num_upcoming_shows": 0
        })
    data.append({
      "city": city.city,
      "state": city.state,
      "venues": venue_per_city
      })
    venue_per_city = []
  return render_template('pages/venues.html', areas=data);

#  List info for specific venue
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # ✔: shows the venue page with the given venue_id
  # ✔: genre data to populate, 
  # past shows and upcoming shows to populate
  base_data = Venue.query.filter_by(id = venue_id).join(City).add_columns(City.city,City.state).first()
  genre_data = Venue.query.select_from(Venue).join(venue_genre).join(Genre).add_columns(Genre.name).filter(Venue.id==venue_id).all()
  genres = []
  for genre in genre_data:
    genres.append(genre[1])

  if base_data is None:
    data={
    "id": venue_id,
    "name": "Venue Not Found",
    "genres": [],
    "address": "",
    "city": "",
    "state": "",
    "phone": "",
    "website": "",
    "facebook_link": "",
    "seeking_talent": "",
    "seeking_description": "",
    "image_link": "",
    "past_shows": [{
      "artist_id": 0,
      "artist_name": "",
      "artist_image_link": "",
      "start_time": "1970-01-01"
    }],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,}
  else:
    data={
      "id": venue_id,
      "name": base_data[0].name,
      "genres": genres,
      "address": base_data[0].address,
      "city": base_data.city,
      "state": base_data.state,
      "phone": base_data[0].phone,
      "website": base_data[0].website,
      "facebook_link": base_data[0].facebook_link,
      "seeking_talent": base_data[0].seeking_talent,
      "seeking_description": base_data[0].seeking_description,
      "image_link": base_data[0].image_link,
      "past_shows": [{
        "artist_id": 0,
        "artist_name": "",
        "artist_image_link": "",
        "start_time": "1970-01-01"
      }],
      "upcoming_shows": [],
      "past_shows_count": 0,
      "upcoming_shows_count": 0,
    }
  return render_template('pages/show_venue.html', venue=data)

# ------------------ Search for venues -------------------------
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # ✔: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  print(search_term)
  search_data = Venue.query.filter(Venue.name.ilike("%"+search_term+"%")).all()
  print(search_data)
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
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

# ------------------ Add venues information -------------------------

#  Create Venue - Get form
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

#  Create Venue - Submit data
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # ✔: insert form data as a new Venue record in the db, instead
  # ✔: modify data to be the data object returned from db insertion
  seekingTalentValue = False
  try:
    nameForm = request.form.get('name')
    addressForm = request.form.get('address')
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
    seekingTalentForm = request.form.get('seeking_talent')
    if seekingTalentForm == 'y':
      seekingTalentValue = True
    seekingDescForm = request.form.get('seeking_description')
    venue = Venue(name = nameForm, address = addressForm, city_id = cityId, phone = phoneForm, image_link = imageLinkForm, 
      facebook_link = fbLinkForm, website= websiteForm, seeking_talent = seekingTalentValue, seeking_description = seekingDescForm)
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
    print(e)
    db.session.rollback()
    # ✔: on unsuccessful db insert, flash an error instead.
    flash('An error occurred: Venue ' + request.form['name'] + ' could not be added!!!')
  finally:
    db.session.close()
  return render_template('pages/home.html')

# ------------------ Edit venues information -------------------------

# Edit Venue - GET
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  search_data = Venue.query.filter_by(id = venue_id).join(City).add_columns(City.city,City.state).first()
  form = VenueForm()
  venue={
    "id": venue_id,
    "name": search_data[0].name,
    "genres": [],
    "address": search_data[0].address,
    "city": search_data.city,
    "state": search_data.state,
    "phone": search_data[0].phone,
    "website": search_data[0].website,
    "facebook_link": search_data[0].facebook_link,
    "seeking_talent": search_data[0].seeking_talent,
    "seeking_description": search_data[0].seeking_description,
    "image_link": search_data[0].image_link
  }
  print(venue)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

# Edit Venue - POST
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  existing_venue = Venue.query.filter_by(id = venue_id).join(City).add_columns(City.city,City.state).first()
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    nameForm = request.form.get('name')
    addressForm = request.form.get('address')
    cityForm = request.form.get('city')
    stateForm = request.form.get('state')
    phoneForm = request.form.get('phone')
    imageLinkForm = request.form.get('image_link')
    fbLinkForm = request.form.get('facebook_link')
    websiteForm = request.form.get('website_link')
    seekingTalentForm = request.form.get('seeking_talent')
    if seekingTalentForm == 'y':
      seekingTalentValue = True
    seekingDescForm = request.form.get('seeking_description')
    existing_venue[0].name = nameForm
    existing_venue[0].address = addressForm
    existing_venue.city = cityForm
    existing_venue.state = stateForm
    existing_venue[0].phone = phoneForm
    existing_venue[0].image_link = imageLinkForm
    existing_venue[0].facebook_link = fbLinkForm
    existing_venue[0].website_link = websiteForm
    existing_venue[0].seeking_talent = seekingTalentValue
    existing_venue[0].seeking_description = seekingDescForm
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully Updated!')
  except Exception as e:
    print(e)
    db.session.rollback()
    # ✔: on unsuccessful db insert, flash an error instead.
    flash('An error occurred: Venue ' + request.form['name'] + ' could not be Updated!!!')
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

# ------------------ Delete venues information -------------------------

#  Delete specific Venue based on a button
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # ✔: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))