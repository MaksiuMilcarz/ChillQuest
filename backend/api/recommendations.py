from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Location, Visit, User
from services.recommendation_engine import get_recommendations, get_personalized_recommendations

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/', methods=['GET'])
def get_general_recommendations():
    """Get general recommendations for non-logged in users"""
    recommendations = get_recommendations()
    return jsonify({
        'recommendations': recommendations
    }), 200

@recommendations_bp.route('/personalized', methods=['GET'])
@jwt_required()
def get_user_recommendations():
    """Get personalized recommendations for logged in users"""
    user_id = get_jwt_identity()
    
    # Check if personalization is turned off
    use_personalization = request.args.get('personalized', 'true').lower() == 'true'
    
    if use_personalization:
        recommendations = get_personalized_recommendations(user_id)
    else:
        # Fall back to general recommendations if personalization is off
        recommendations = get_recommendations()
        
    return jsonify({
        'recommendations': recommendations,
        'personalized': use_personalization
    }), 200