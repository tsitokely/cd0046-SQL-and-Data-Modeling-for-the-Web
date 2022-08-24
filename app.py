#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

from models.models import db, Genre, Artist, Venue, City, Show, venue_genre, artist_genre
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
moment = Moment(app)

migrate = Migrate(app,db)


# ✔: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

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

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

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
  # TODO: genre data to populate, past shows and upcoming shows to populate
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

#  Search for venues
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

#  Artists
#  ----------------------------------------------------------------

#  List all artists
@app.route('/artists')
def artists():
  # ✔: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

#  Search for artists
@app.route('/artists/search', methods=['POST'])
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

@app.route('/artists/<int:artist_id>')
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
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
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

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
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

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
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
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
