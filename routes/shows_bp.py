from flask import Blueprint

from controllers.shows import shows, create_shows, create_show_submission

shows_bp = Blueprint('shows_bp', __name__)

shows_bp.route('/shows')(shows)
shows_bp.route('/shows/create')(create_shows)
shows_bp.route('/shows/create', methods=['POST'])(create_show_submission)