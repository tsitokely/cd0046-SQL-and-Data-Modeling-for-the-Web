from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL
from enum import Enum

def choices(cls):
    return [(choice.value, choice.name ) for choice in cls]

Genre = Enum(
    value = 'Genres',
    names =[
        ('Alternative', 1),
        ('Blues', 2),
        ('Classical', 3),
        ('Country', 4),
        ('Electronic', 5),
        ('Folk', 6),
        ('Funk', 7),
        ('Hip-Hop', 8),
        ('HipHop', 8),
        ('Heavy Metal', 9),
        ('HeavyMetal', 9),
        ('Instrumental', 10),
        ('Jazz', 11),
        ('Musical Theatre', 12),
        ('MusicalTheatre', 12),
        ('Pop', 13),
        ('Punk', 14),
        ('R&B', 15),
        ('RB', 15),
        ('Reggae', 16),
        ('Rock n Roll', 17),
        ('RocknRoll', 17),
        ('Soul', 18),
        ('Other', 19)
    ])

State = Enum(
    value = 'States',
    names =[
        ('AL', 'AL'),
        ('AK', 'AK'),
        ('AZ', 'AZ'),
        ('AR', 'AR'),
        ('CA', 'CA'),
        ('CO', 'CO'),
        ('CT', 'CT'),
        ('DE', 'DE'),
        ('DC', 'DC'),
        ('FL', 'FL'),
        ('GA', 'GA'),
        ('HI', 'HI'),
        ('ID', 'ID'),
        ('IL', 'IL'),
        ('IN', 'IN'),
        ('IA', 'IA'),
        ('KS', 'KS'),
        ('KY', 'KY'),
        ('LA', 'LA'),
        ('ME', 'ME'),
        ('MT', 'MT'),
        ('NE', 'NE'),
        ('NV', 'NV'),
        ('NH', 'NH'),
        ('NJ', 'NJ'),
        ('NM', 'NM'),
        ('NY', 'NY'),
        ('NC', 'NC'),
        ('ND', 'ND'),
        ('OH', 'OH'),
        ('OK', 'OK'),
        ('OR', 'OR'),
        ('MD', 'MD'),
        ('MA', 'MA'),
        ('MI', 'MI'),
        ('MN', 'MN'),
        ('MS', 'MS'),
        ('MO', 'MO'),
        ('PA', 'PA'),
        ('RI', 'RI'),
        ('SC', 'SC'),
        ('SD', 'SD'),
        ('TN', 'TN'),
        ('TX', 'TX'),
        ('UT', 'UT'),
        ('VT', 'VT'),
        ('VA', 'VA'),
        ('WA', 'WA'),
        ('WV', 'WV'),
        ('WI', 'WI'),
        ('WY', 'WY')
    ])

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=choices(State)
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=choices(Genre)
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link'
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if self.state.data not in dict(choices(State)).keys():
            self.state.errors.append('Invalid state.')
            return False
        if self.genres.data not in dict(choices(State)).values():
            self.genres.errors.append('Invalid genre.')
            return False
        return True

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=choices(State)
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=choices(Genre)
     )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
     )

    website_link = StringField(
        'website_link'
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if self.state.data not in dict(choices(State)).keys():
            self.state.errors.append('Invalid state.')
            return False
        if self.genres.data not in dict(choices(State)).values():
            self.genres.errors.append('Invalid genre.')
            return False
        return True

