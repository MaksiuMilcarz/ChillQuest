from models import Location, Visit, User, db
from sqlalchemy import func
from collections import Counter

def get_recommendations(limit=10):
    """
    Get general recommendations based on highest ratings
    Returns a list of location dictionaries
    """
    # Get the highest rated locations
    top_locations = Location.query.order_by(Location.rating.desc()).limit(limit).all()
    return [location.to_dict() for location in top_locations]

def get_personalized_recommendations(user_id, limit=10):
    """
    Get personalized recommendations for a user based on their visit history
    Uses a simple content-based filtering approach
    
    Think of this like a "if you liked this, you might also like..." approach
    """
    user = User.query.get(user_id)
    if not user:
        return get_recommendations(limit)  # Fallback to general recommendations
    
    # Get user's visits
    user_visits = Visit.query.filter_by(user_id=user_id).all()
    
    if not user_visits:
        return get_recommendations(limit)  # No visit history, use general recommendations
    
    # Extract locations the user has visited and their ratings
    visited_location_ids = [visit.location_id for visit in user_visits]
    
    # If user has rated locations, use their preferences
    user_rated_visits = [visit for visit in user_visits if visit.rating is not None]
    
    if user_rated_visits:
        # Find location types that the user rates highly
        location_preferences = {}
        for visit in user_rated_visits:
            location = Location.query.get(visit.location_id)
            if location:
                if location.type not in location_preferences:
                    location_preferences[location.type] = {'count': 0, 'rating_sum': 0}
                location_preferences[location.type]['count'] += 1
                location_preferences[location.type]['rating_sum'] += visit.rating
        
        # Calculate average rating per type
        for loc_type in location_preferences:
            if location_preferences[loc_type]['count'] > 0:
                location_preferences[loc_type]['avg_rating'] = (
                    location_preferences[loc_type]['rating_sum'] / 
                    location_preferences[loc_type]['count']
                )
            else:
                location_preferences[loc_type]['avg_rating'] = 0
        
        # Sort types by preference
        preferred_types = sorted(
            location_preferences.keys(),
            key=lambda x: location_preferences[x]['avg_rating'],
            reverse=True
        )
        
        # Find similar locations of preferred types that the user hasn't visited
        recommendations = []
        for loc_type in preferred_types:
            similar_locations = Location.query.filter(
                Location.type == loc_type,
                ~Location.id.in_(visited_location_ids)
            ).order_by(Location.rating.desc()).limit(limit).all()
            
            recommendations.extend(similar_locations)
            if len(recommendations) >= limit:
                break
        
        # If we still need more recommendations, add some top-rated ones
        if len(recommendations) < limit:
            additional = Location.query.filter(
                ~Location.id.in_(visited_location_ids),
                ~Location.id.in_([loc.id for loc in recommendations])
            ).order_by(Location.rating.desc()).limit(limit - len(recommendations)).all()
            
            recommendations.extend(additional)
        
        return [location.to_dict() for location in recommendations[:limit]]
    
    # If no ratings, recommend top-rated locations user hasn't visited
    return [
        location.to_dict() 
        for location in Location.query.filter(
            ~Location.id.in_(visited_location_ids)
        ).order_by(Location.rating.desc()).limit(limit).all()
    ]