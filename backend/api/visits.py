from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Visit, Location, User

visits_bp = Blueprint('visits', __name__)

@visits_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_visits():
    """Get all visits for the current user with location details"""
    try:
        # Get user ID - convert string to int if needed
        current_user_id = get_jwt_identity()
        print(f"Identity from token: {current_user_id}, type: {type(current_user_id)}")
        
        # Convert to integer if it's a string
        try:
            user_id = int(current_user_id)
        except (ValueError, TypeError):
            user_id = current_user_id
            
        print(f"Fetching visits for user ID: {user_id}")
            
        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            print(f"User with ID {user_id} not found")
            return jsonify({'message': 'User not found'}), 404
        
        print(f"User found: {user.username}")
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
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Error processing request: {str(e)}'}), 500

@visits_bp.route('/', methods=['POST'])
@jwt_required()
def add_visit():
    """Add or update a visit for the current user"""
    try:
        # Get user ID from token and convert to int if needed
        current_user_id = get_jwt_identity()
        try:
            user_id = int(current_user_id)
        except (ValueError, TypeError):
            user_id = current_user_id
            
        print(f"Adding visit for user ID: {user_id}")
        
        # Get JSON data
        data = request.get_json(force=True)
        print(f"Visit data received: {data}")
            
        if not data:
            print("No JSON data provided")
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
        
        # Check for rating (required for new visits)
        is_new_visit = not Visit.query.filter_by(user_id=user_id, location_id=location_id).first()
        if is_new_visit and ('rating' not in data or data['rating'] is None):
            print("Missing required rating for new visit")
            return jsonify({'message': 'Rating is required when adding a new visit'}), 400
            
        if is_new_visit and data.get('rating') is not None:
            try:
                rating = int(data['rating'])
                if rating < 1 or rating > 5:
                    print(f"Invalid rating value: {rating}")
                    return jsonify({'message': 'Rating must be between 1 and 5'}), 400
            except (ValueError, TypeError):
                print(f"Invalid rating format: {data['rating']}")
                return jsonify({'message': 'Rating must be a number between 1 and 5'}), 400
        
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
            if 'rating' in data and data['rating'] is not None:
                try:
                    rating = int(data['rating'])
                    if 1 <= rating <= 5:
                        existing_visit.rating = rating
                    else:
                        print(f"Invalid rating value for update: {rating}")
                except (ValueError, TypeError):
                    print(f"Invalid rating format for update: {data['rating']}")
            
            if 'notes' in data:
                existing_visit.notes = data['notes']
            
            db.session.commit()
            
            # Get the location data to include in response
            location_data = location.to_dict()
            visit_data = existing_visit.to_dict()
            visit_data['location'] = location_data
            
            return jsonify({
                'message': 'Visit updated',
                'visit': visit_data
            }), 200
        
        # Create new visit - ensure rating is provided
        if 'rating' not in data or data['rating'] is None:
            return jsonify({'message': 'Rating is required for new visits'}), 400
            
        visit = Visit(
            user_id=user_id,
            location_id=data['location_id'],
            rating=data['rating'],
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
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'message': f'Error processing request: {str(e)}'}), 500

@visits_bp.route('/<int:visit_id>', methods=['DELETE'])
@jwt_required()
def delete_visit(visit_id):
    """Delete a specific visit belonging to the current user"""
    try:
        # Get user ID from token and convert to int if needed
        current_user_id = get_jwt_identity()
        try:
            user_id = int(current_user_id)
        except (ValueError, TypeError):
            user_id = current_user_id
            
        print(f"Delete visit - User: {user_id}, Visit ID: {visit_id}")
        visit = Visit.query.filter_by(id=visit_id, user_id=user_id).first()
        
        if not visit:
            return jsonify({'message': 'Visit not found or unauthorized'}), 404
        
        db.session.delete(visit)
        db.session.commit()
        print(f"Deleted visit ID: {visit_id}")
        
        return jsonify({'message': 'Visit deleted'}), 200
    except Exception as e:
        print(f"Error in delete_visit: {str(e)}")
        db.session.rollback()
        return jsonify({'message': f'Error processing request: {str(e)}'}), 500