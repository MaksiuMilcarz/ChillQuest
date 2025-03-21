from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models import db, Visit, Location, User
import traceback

visits_bp = Blueprint('visits', __name__)

@visits_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_visits():
    """Get all visits for the current user with location details"""
    try:
        # Debug token
        try:
            verify_jwt_in_request()
            print("JWT verification successful")
        except Exception as jwt_err:
            print(f"JWT verification error: {jwt_err}")
            return jsonify({'message': 'Invalid authentication token'}), 401
        
        # Get user ID from token
        user_id = get_jwt_identity()
        print(f"JWT extracted user_id: {user_id}")
        
        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            print(f"User with ID {user_id} not found")
            return jsonify({'message': 'User not found'}), 404
        
        print(f"Fetching visits for user ID: {user_id}, username: {user.username}")
        visits = Visit.query.filter_by(user_id=user_id).all()
        print(f"Found {len(visits)} visits")
        
        # Include location details for each visit
        result = []
        for visit in visits:
            visit_data = visit.to_dict()
            location = Location.query.get(visit.location_id)
            if location:
                visit_data['location'] = location.to_dict()
                print(f"Added location data for visit to {location.name}")
            else:
                visit_data['location'] = {'id': visit.location_id, 'name': 'Unknown Location'}
                print(f"Warning: Location with ID {visit.location_id} not found")
            result.append(visit_data)
        
        print(f"Returning {len(result)} visit records with location data")
        return jsonify({
            'visits': result
        }), 200
    except Exception as e:
        print(f"Error in get_user_visits: {str(e)}")
        traceback.print_exc()
        return jsonify({'message': f'Error processing request: {str(e)}'}), 500

@visits_bp.route('/', methods=['POST'])
@jwt_required()
def add_visit():
    """Add or update a visit for the current user"""
    try:
        # Debug the request
        print(f"POST /visits/ request received")
        print(f"Request headers: {request.headers}")
        print(f"Request mimetype: {request.mimetype}")
        print(f"Request data raw: {request.data}")
        
        user_id = get_jwt_identity()
        print(f"JWT extracted user_id for add_visit: {user_id}")
        
        # Get JSON data with better error handling
        data = request.get_json(force=True, silent=True)
        print(f"Parsed JSON data: {data}")
        
        if not data:
            print("No JSON data in request")
            return jsonify({'message': 'No JSON data provided'}), 400
            
        # Validate location_id
        if 'location_id' not in data:
            print("Missing location_id in request")
            return jsonify({'message': 'location_id is required'}), 400
        
        # Ensure location_id is an integer
        try:
            location_id = int(data['location_id'])
            data['location_id'] = location_id
        except (ValueError, TypeError):
            print(f"Invalid location_id format: {data.get('location_id')}")
            return jsonify({'message': 'location_id must be an integer'}), 400
        
        print(f"Processing visit - User: {user_id}, Location: {data['location_id']}")
        
        # Check if location exists
        location = Location.query.get(data['location_id'])
        if not location:
            print(f"Location {data['location_id']} not found")
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
            print(f"Visit updated successfully")
            
            # Get the location data to include in response
            location_data = location.to_dict()
            visit_data = existing_visit.to_dict()
            visit_data['location'] = location_data
            
            return jsonify({
                'message': 'Visit updated',
                'visit': visit_data
            }), 200
        
        # Create new visit
        visit = Visit(
            user_id=user_id,
            location_id=data['location_id'],
            rating=data.get('rating'),
            notes=data.get('notes', '')
        )
        
        db.session.add(visit)
        db.session.commit()
        print(f"Created new visit ID: {visit.id}")
        
        # Get the location data to include in response
        location_data = location.to_dict()
        visit_data = visit.to_dict()
        visit_data['location'] = location_data
        
        return jsonify({
            'message': 'Visit added',
            'visit': visit_data
        }), 201
    except Exception as e:
        print(f"Error in add_visit: {str(e)}")
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'message': f'Error processing request: {str(e)}'}), 500

@visits_bp.route('/<int:visit_id>', methods=['DELETE'])
@jwt_required()
def delete_visit(visit_id):
    """Delete a visit"""
    try:
        print(f"DELETE /visits/{visit_id} request received")
        user_id = get_jwt_identity()
        print(f"JWT extracted user_id: {user_id}")
        
        # Find visit by ID and user
        visit = Visit.query.filter_by(id=visit_id, user_id=user_id).first()
        
        if not visit:
            print(f"Visit {visit_id} not found for user {user_id}")
            return jsonify({'message': 'Visit not found or not owned by user'}), 404
        
        print(f"Deleting visit {visit_id} for location {visit.location_id}")
        db.session.delete(visit)
        db.session.commit()
        
        return jsonify({'message': 'Visit deleted'}), 200
    except Exception as e:
        print(f"Error deleting visit: {str(e)}")
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'message': f'Error processing request: {str(e)}'}), 500