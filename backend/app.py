from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import db, User, Location, Visit
from config import Config
from auth.routes import auth_bp
from api.locations import locations_bp
from api.visits import visits_bp
from api.recommendations import recommendations_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    
    # Configure CORS properly to allow cross-origin requests
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    
    # Add CORS headers to every response
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Handle OPTIONS preflight requests
    @app.route('/api/<path:path>', methods=['OPTIONS'])
    def handle_preflight(path):
        response = app.make_default_options_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(locations_bp, url_prefix='/api/locations')
    app.register_blueprint(visits_bp, url_prefix='/api/visits')
    app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
    
    # Add a health check endpoint
    @app.route('/api/health')
    def health_check():
        users_count = User.query.count()
        locations_count = Location.query.count()
        visits_count = Visit.query.count()
        
        return jsonify({
            "status": "healthy",
            "database_path": app.config['SQLALCHEMY_DATABASE_URI'],
            "users_count": users_count,
            "locations_count": locations_count,
            "visits_count": visits_count
        })
    
    # Add a debug endpoint
    @app.route('/api/debug/users')
    def debug_users():
        users = User.query.all()
        return jsonify({
            "users": [{"id": u.id, "username": u.username, "email": u.email} for u in users]
        })
    
    return app

def seed_locations():
    """Seed the database with some initial locations"""
    
    locations = [
        # Nature locations
        {
            'name': 'Grand Canyon',
            'city': 'Arizona',
            'country': 'USA',
            'description': 'Steep-sided canyon carved by the Colorado River.',
            'price_level': 2,
            'type': 'nature',
            'rating': 4.9,
            'latitude': 36.1069,
            'longitude': -112.1129
        },
        {
            'name': 'Amazon Rainforest',
            'city': 'Manaus',
            'country': 'Brazil',
            'description': 'Largest tropical rainforest in the world.',
            'price_level': 4,
            'type': 'nature',
            'rating': 4.8,
            'latitude': -3.4653,
            'longitude': -62.2159
        },
        {
            'name': 'Uluru',
            'city': 'Northern Territory',
            'country': 'Australia',
            'description': 'Large sandstone rock formation sacred to indigenous people.',
            'price_level': 3,
            'type': 'nature',
            'rating': 4.8,
            'latitude': -25.3444,
            'longitude': 131.0369
        },
        {
            'name': 'Mount Everest',
            'city': 'Solukhumbu',
            'country': 'Nepal',
            'description': 'Earth\'s highest mountain above sea level.',
            'price_level': 5,
            'type': 'nature',
            'rating': 4.9,
            'latitude': 27.9881,
            'longitude': 86.9250
        },
        {
            'name': 'Northern Lights',
            'city': 'Tromsø',
            'country': 'Norway',
            'description': 'Natural light display in the sky, particularly in high-latitude regions.',
            'price_level': 3,
            'type': 'nature',
            'rating': 4.9,
            'latitude': 69.6492,
            'longitude': 18.9553
        },
        
        # Recreational locations
        {
            'name': 'Walt Disney World',
            'city': 'Orlando',
            'country': 'USA',
            'description': 'Entertainment complex with theme parks and resorts.',
            'price_level': 4,
            'type': 'recreational',
            'rating': 4.7,
            'latitude': 28.3852,
            'longitude': -81.5639
        },
        {
            'name': 'Bondi Beach',
            'city': 'Sydney',
            'country': 'Australia',
            'description': 'Popular beach known for surfing and swimming.',
            'price_level': 1,
            'type': 'recreational',
            'rating': 4.5,
            'latitude': -33.8915,
            'longitude': 151.2767
        },
        {
            'name': 'Ski Dubai',
            'city': 'Dubai',
            'country': 'UAE',
            'description': 'Indoor ski resort with 22,500 square meters of indoor ski area.',
            'price_level': 4,
            'type': 'recreational',
            'rating': 4.4,
            'latitude': 25.1182,
            'longitude': 55.2004
        },
        {
            'name': 'Central Park',
            'city': 'New York',
            'country': 'USA',
            'description': 'Urban park offering various recreational activities.',
            'price_level': 1,
            'type': 'recreational',
            'rating': 4.8,
            'latitude': 40.7812,
            'longitude': -73.9665
        },
        {
            'name': 'Universal Studios',
            'city': 'Los Angeles',
            'country': 'USA',
            'description': 'Film studio and theme park with various attractions.',
            'price_level': 4,
            'type': 'recreational',
            'rating': 4.6,
            'latitude': 34.1381,
            'longitude': -118.3534
        },
        
        # Nightlife locations
        {
            'name': 'Berghain',
            'city': 'Berlin',
            'country': 'Germany',
            'description': 'World-famous techno club known for its intense nightlife.',
            'price_level': 3,
            'type': 'nightlife',
            'rating': 4.8,
            'latitude': 52.5111,
            'longitude': 13.4432
        },
        {
            'name': 'Pacha',
            'city': 'Ibiza',
            'country': 'Spain',
            'description': 'Iconic nightclub established in 1973, known for electronic music.',
            'price_level': 4,
            'type': 'nightlife',
            'rating': 4.7,
            'latitude': 38.9181,
            'longitude': 1.4492
        },
        {
            'name': 'Cavo Paradiso',
            'city': 'Mykonos',
            'country': 'Greece',
            'description': 'Open-air club perched on a cliff with views of the Aegean Sea.',
            'price_level': 5,
            'type': 'nightlife',
            'rating': 4.8,
            'latitude': 37.4088,
            'longitude': 25.3454
        },
        {
            'name': 'XS Nightclub',
            'city': 'Las Vegas',
            'country': 'USA',
            'description': 'Luxurious nightclub at the Encore hotel with indoor and outdoor space.',
            'price_level': 5,
            'type': 'nightlife',
            'rating': 4.6,
            'latitude': 36.1293,
            'longitude': -115.1686
        },
        {
            'name': 'Omnia',
            'city': 'Las Vegas',
            'country': 'USA',
            'description': 'Multilevel venue with electronic music and world-renowned DJs.',
            'price_level': 5,
            'type': 'nightlife',
            'rating': 4.5,
            'latitude': 36.1160,
            'longitude': -115.1740
        },
        {
            'name': 'Ministry of Sound',
            'city': 'London',
            'country': 'UK',
            'description': 'Iconic nightclub dedicated to house music and other electronic genres.',
            'price_level': 3,
            'type': 'nightlife',
            'rating': 4.6,
            'latitude': 51.4926,
            'longitude': -0.0998
        },
        {
            'name': 'Zouk',
            'city': 'Singapore',
            'country': 'Singapore',
            'description': 'Award-winning nightclub playing diverse electronic dance music.',
            'price_level': 4,
            'type': 'nightlife',
            'rating': 4.7,
            'latitude': 1.2914,
            'longitude': 103.8607
        },
        {
            'name': 'Fabric',
            'city': 'London',
            'country': 'UK',
            'description': 'Renowned London nightclub known for electronic music.',
            'price_level': 3,
            'type': 'nightlife',
            'rating': 4.7,
            'latitude': 51.5204,
            'longitude': -0.1018
        },
        {
            'name': 'Green Valley',
            'city': 'Camboriú',
            'country': 'Brazil',
            'description': 'Open-air superclub voted as one of the best clubs in the world.',
            'price_level': 4,
            'type': 'nightlife',
            'rating': 4.8,
            'latitude': -26.9879,
            'longitude': -48.6324
        },
        {
            'name': 'Hakkasan',
            'city': 'Las Vegas',
            'country': 'USA',
            'description': 'Five-story nightclub and restaurant with world-class DJs.',
            'price_level': 5,
            'type': 'nightlife',
            'rating': 4.5,
            'latitude': 36.1023,
            'longitude': -115.1703
        },
        
        # Culture locations
        {
            'name': 'Louvre Museum',
            'city': 'Paris',
            'country': 'France',
            'description': 'World\'s largest art museum and historic monument.',
            'price_level': 3,
            'type': 'culture',
            'rating': 4.7,
            'latitude': 48.8606,
            'longitude': 2.3376
        },
        {
            'name': 'British Museum',
            'city': 'London',
            'country': 'UK',
            'description': 'Museum with a vast collection of world art and artifacts.',
            'price_level': 1,
            'type': 'culture',
            'rating': 4.7,
            'latitude': 51.5194,
            'longitude': -0.1269
        },
        {
            'name': 'Acropolis',
            'city': 'Athens',
            'country': 'Greece',
            'description': 'Ancient citadel with Parthenon temple.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.8,
            'latitude': 37.9715,
            'longitude': 23.7267
        },
        {
            'name': 'Smithsonian Museums',
            'city': 'Washington DC',
            'country': 'USA',
            'description': 'World\'s largest museum and research complex.',
            'price_level': 1,
            'type': 'culture',
            'rating': 4.8,
            'latitude': 38.8921,
            'longitude': -77.0241
        },
        {
            'name': 'Sydney Opera House',
            'city': 'Sydney',
            'country': 'Australia',
            'description': 'Iconic performing arts center with distinctive sail-like design.',
            'price_level': 3,
            'type': 'culture',
            'rating': 4.6,
            'latitude': -33.8568,
            'longitude': 151.2153
        },
        
        # Food locations
        {
            'name': 'Borough Market',
            'city': 'London',
            'country': 'UK',
            'description': 'One of London\'s oldest food markets with various vendors.',
            'price_level': 2,
            'type': 'food',
            'rating': 4.6,
            'latitude': 51.5055,
            'longitude': -0.0911
        },
        {
            'name': 'Tsukiji Outer Market',
            'city': 'Tokyo',
            'country': 'Japan',
            'description': 'Market area with shops and restaurants specializing in fresh seafood.',
            'price_level': 3,
            'type': 'food',
            'rating': 4.7,
            'latitude': 35.6654,
            'longitude': 139.7707
        },
        {
            'name': 'Pike Place Market',
            'city': 'Seattle',
            'country': 'USA',
            'description': 'Historic farmers market overlooking Elliott Bay.',
            'price_level': 2,
            'type': 'food',
            'rating': 4.7,
            'latitude': 47.6097,
            'longitude': -122.3422
        },
        {
            'name': 'Mercado de San Miguel',
            'city': 'Madrid',
            'country': 'Spain',
            'description': 'Historic covered market with tapas bars and food stalls.',
            'price_level': 3,
            'type': 'food',
            'rating': 4.5,
            'latitude': 40.4153,
            'longitude': -3.7091
        },
        {
            'name': 'Jemaa el-Fnaa',
            'city': 'Marrakech',
            'country': 'Morocco',
            'description': 'Square with food stalls, performers, and market vendors.',
            'price_level': 2,
            'type': 'food',
            'rating': 4.6,
            'latitude': 31.6258,
            'longitude': -7.9891
        }
    ]
    
    for loc_data in locations:
        location = Location(**loc_data)
        db.session.add(location)
    
    db.session.commit()
    
    # After locations are added, create a demo user with visits
    create_demo_user()

def create_demo_user():
    """Create a demo user with predefined visits focused on nightlife"""
    import random
    from datetime import datetime, timedelta
    
    # Check if demo user already exists
    if User.query.filter_by(username='demouser').first():
        return
    
    # Create demo user
    demo_user = User(
        username='demouser',
        email='demo@example.com',
        password='password123'
    )
    db.session.add(demo_user)
    db.session.flush()  # To get the user ID
    
    # Current date for reference
    now = datetime.utcnow()
    
    # First, add visits to nightlife locations with high ratings
    nightlife_locations = Location.query.filter_by(type='nightlife').all()
    
    for i, location in enumerate(nightlife_locations):
        # Create a visit with a random date in the past year
        days_ago = random.randint(1, 200)  # More recent visits
        visit_date = now - timedelta(days=days_ago)
        
        # Assign a high rating (nightlife enthusiast)
        rating = random.choice([4, 5])  # Prefers nightlife venues
        
        # Create enthusiastic notes for nightlife venues
        notes = ""
        if rating == 5:
            notes = f"Amazing night at {location.name}! The music and atmosphere were incredible. Definitely coming back!"
        elif rating == 4:
            notes = f"Great experience at {location.name}. Good DJs and vibrant crowd."
        
        visit = Visit(
            user_id=demo_user.id,
            location_id=location.id,
            visit_date=visit_date,
            rating=rating,
            notes=notes
        )
        db.session.add(visit)
    
    # Add some visits to other types of locations with lower ratings
    other_locations = Location.query.filter(Location.type != 'nightlife').limit(10).all()
    
    for i, location in enumerate(other_locations):
        # Create a visit with a random date in the past year
        days_ago = random.randint(200, 365)  # Older visits
        visit_date = now - timedelta(days=days_ago)
        
        # Assign a lower rating (less enthusiastic about non-nightlife venues)
        rating = random.choice([2, 3, 4])
        
        # Create less enthusiastic notes for other venue types
        notes = ""
        if location.type == 'nature':
            notes = f"Nice place, but a bit too quiet for my taste. {location.name} was pretty though."
        elif location.type == 'culture':
            notes = f"Interesting visit to {location.name}, but wished there was more excitement."
        elif location.type == 'food':
            notes = f"The food at {location.name} was good. Decent atmosphere."
        else:
            notes = f"Visited {location.name}. It was okay."
        
        visit = Visit(
            user_id=demo_user.id,
            location_id=location.id,
            visit_date=visit_date,
            rating=rating,
            notes=notes
        )
        db.session.add(visit)
    
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)