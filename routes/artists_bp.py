from flask import Blueprint

from controllers.artists import artists, search_artists, show_artist, edit_artist, edit_artist_submission, create_artist_form, create_artist_submission

artists_bp = Blueprint('artists_bp', __name__)

artists_bp.route('/artists')(artists)
artists_bp.route('/artists/search', methods=['POST'])(search_artists)
artists_bp.route('/artists/<int:artist_id>')(show_artist)
artists_bp.route('/artists/<int:artist_id>/edit', methods=['GET'])(edit_artist)
artists_bp.route('/artists/<int:artist_id>/edit', methods=['POST'])(edit_artist_submission)
artists_bp.route('/artists/create', methods=['GET'])(create_artist_form)
artists_bp.route('/artists/create', methods=['POST'])(create_artist_submission)