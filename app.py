#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, render_template
from flask_moment import Moment
from flask_migrate import Migrate
from models.models import db
from routes.artists_bp import artists_bp
from routes.shows_bp import shows_bp
from routes.venues_bp import venues_bp
import babel
import dateutil.parser
from logging import Formatter, FileHandler
import logging

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
moment = Moment(app)
migrate = Migrate(app,db)

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
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

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# Seed genre table based on a static list
from models.models import Genre
@app.before_first_request
def seed():
  try:
    genre_data = ('Alternative','Blues','Classical','Country','Electronic',
      'Folk','Funk','Hip-Hop','Heavy Metal','Instrumental',
      'Jazz','Musical Theatre','Pop','Punk','R&B','Reggae',
      'Rock n Roll','Soul','Other')
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

app.register_blueprint(artists_bp, url_prefix='/')
app.register_blueprint(shows_bp, url_prefix='/')
app.register_blueprint(venues_bp, url_prefix='/')

# Main route
@app.route('/')
def index():
  return render_template('pages/home.html')
# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
