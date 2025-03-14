from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import db, Location

locations_bp = Blueprint('locations', __name__)

@locations_bp.route('/', methods=['GET'])
def get_all_locations():
    locations = Location.query.all()
    return jsonify({
        'locations': [location.to_dict() for location in locations]
    }), 200

@locations_bp.route('/<int:location_id>', methods=['GET'])
def get_location(location_id):
    location = Location.query.get(location_id)
    
    if not location:
        return jsonify({'message': 'Location not found'}), 404
    
    return jsonify(location.to_dict()), 200

@locations_bp.route('/search', methods=['GET'])
def search_locations():
    query = request.args.get('q', '')
    location_type = request.args.get('type', None)
    
    # Start with base query
    base_query = Location.query
    
    # Add filters
    if query:
        base_query = base_query.filter(
            (Location.name.ilike(f'%{query}%')) |
            (Location.city.ilike(f'%{query}%')) |
            (Location.country.ilike(f'%{query}%'))
        )
    
    if location_type:
        base_query = base_query.filter(Location.type == location_type)
    
    # Execute query
    locations = base_query.all()
    
    return jsonify({
        'locations': [location.to_dict() for location in locations]
    }), 200