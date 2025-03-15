from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Visit, Location, User

visits_bp = Blueprint('visits', __name__)

@visits_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_visits():
    """Get all visits for the current user with location details"""
    user_id = get_jwt_identity()
    
    # Verify user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    print(f"Fetching visits for user ID: {user_id}")
    visits = Visit.query.filter_by(user_id=user_id).all()
    print(f"Found {len(visits)} visits")
    
    # Include location details for each visit
    result = []
    for visit in visits:
        visit_data = visit.to_dict()
        location = Location.query.get(visit.location_id)
        if location:
            visit_data['location'] = location.to_dict()
        else:
            visit_data['location'] = {'id': visit.location_id, 'name': 'Unknown Location'}
        result.append(visit_data)
    
    return jsonify({
        'visits': result
    }), 200

@visits_bp.route('/', methods=['POST'])
@jwt_required()
def add_visit():
    """Add or update a visit for the current user"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Improved validation with better error handling
    if not data:
        return jsonify({'message': 'No JSON data provided'}), 400
        
    if 'location_id' not in data:
        return jsonify({'message': 'location_id is required'}), 400
    
    # Ensure location_id is an integer
    try:
        location_id = int(data['location_id'])
        data['location_id'] = location_id
    except (ValueError, TypeError):
        return jsonify({'message': 'location_id must be an integer'}), 400
    
    print(f"Add/update visit - User: {user_id}, Location: {data['location_id']}")
    
    # Check if location exists
    location = Location.query.get(data['location_id'])
    if not location:
        return jsonify({'message': 'Location not found'}), 404
    
    # Check if visit already exists
    existing_visit = Visit.query.filter_by(
        user_id=user_id, 
        location_id=data['location_id']
    ).first()
    
    if existing_visit:
        # Update existing visit
        print(f"Updating existing visit ID: {existing_visit.id}")
        if 'rating' in data:
            existing_visit.rating = data['rating']
        if 'notes' in data:
            existing_visit.notes = data['notes']
        
        db.session.commit()
        return jsonify({
            'message': 'Visit updated',
            'visit': existing_visit.to_dict()
        }), 200
    
    # Create new visit
    visit = Visit(
        user_id=user_id,
        location_id=data['location_id'],
        rating=data.get('rating'),
        notes=data.get('notes')
    )
    
    db.session.add(visit)
    db.session.commit()
    print(f"Created new visit ID: {visit.id}")
    
    return jsonify({
        'message': 'Visit added',
        'visit': visit.to_dict()
    }), 201

@visits_bp.route('/<int:visit_id>', methods=['DELETE'])
@jwt_required()
def delete_visit(visit_id):
    """Delete a specific visit belonging to the current user"""
    user_id = get_jwt_identity()
    
    print(f"Delete visit - User: {user_id}, Visit ID: {visit_id}")
    visit = Visit.query.filter_by(id=visit_id, user_id=user_id).first()
    
    if not visit:
        return jsonify({'message': 'Visit not found or unauthorized'}), 404
    
    db.session.delete(visit)
    db.session.commit()
    print(f"Deleted visit ID: {visit_id}")
    
    return jsonify({'message': 'Visit deleted'}), 200