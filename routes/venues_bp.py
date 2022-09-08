from flask import Blueprint

from controllers.venues import venues, show_venue, search_venues, create_venue_form,create_venue_submission,edit_venue,edit_venue_submission,delete_venue
venues_bp = Blueprint('venues_bp', __name__)

venues_bp.route('/venues')(venues)
venues_bp.route('/venues/<int:venue_id>')(show_venue)
venues_bp.route('/venues/search', methods=['POST'])(search_venues)
venues_bp.route('/venues/create', methods=['GET'])(create_venue_form)
venues_bp.route('/venues/create', methods=['POST'])(create_venue_submission)
venues_bp.route('/venues/<int:venue_id>/edit', methods=['GET'])(edit_venue)
venues_bp.route('/venues/<int:venue_id>/edit', methods=['POST'])(edit_venue_submission)
venues_bp.route('/venues/<venue_id>', methods=['DELETE'])(delete_venue)