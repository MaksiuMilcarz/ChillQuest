from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity
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
    
    # Configure JWT
    jwt = JWTManager(app)
    
    # Modify JWT error handlers for better debugging
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"Invalid token error: {error}")
        return jsonify({
            'message': 'Invalid token',
            'error': str(error)
        }), 401
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        print(f"No auth token provided: {error}")
        return jsonify({
            'message': 'No auth token provided',
            'error': str(error)
        }), 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print(f"Token expired: {jwt_payload}")
        return jsonify({
            'message': 'Token has expired',
            'error': 'token_expired'
        }), 401
    
    # Configure CORS with more permissive settings
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        }
    })
    
    # Add a test endpoint to verify JWT is working correctly
    @app.route('/api/auth/verify', methods=['GET'])
    def verify_auth():
        auth_header = request.headers.get('Authorization', 'None')
        return jsonify({
            "message": "Auth headers received",
            "auth_header": auth_header,
            "all_headers": dict(request.headers)
        })
    
    # Add a test endpoint for debugging
    @app.route('/api/test', methods=['GET'])
    def test_endpoint():
        """Simple endpoint that returns a 200 OK with a JSON message"""
        print("Test endpoint called!")
        return jsonify({
            "message": "Backend API is working correctly",
            "status": "success"
        })
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(locations_bp, url_prefix='/api/locations')
    app.register_blueprint(visits_bp, url_prefix='/api/visits')
    app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
    # Add a health check endpoint
    @app.route('/api/health')
    def health_check():
        try:
            users_count = User.query.count()
            locations_count = Location.query.count()
            visits_count = Visit.query.count()
            
            return jsonify({
                "status": "healthy",
                "database_path": app.config['SQLALCHEMY_DATABASE_URI'],
                "users_count": users_count,
                "locations_count": locations_count,
                "visits_count": visits_count,
                "jwt_config": {
                    "token_location": app.config['JWT_TOKEN_LOCATION'],
                    "header_name": app.config['JWT_HEADER_NAME'],
                    "header_type": app.config['JWT_HEADER_TYPE'],
                }
            })
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "error": str(e)
            }), 500
    
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
    
    # Additional locations to add to the existing seed_locations function in app.py

    additional_locations = [
        # More Nature locations
        {
            'name': 'Great Barrier Reef',
            'city': 'Queensland',
            'country': 'Australia',
            'description': 'The world\'s largest coral reef system, visible from space.',
            'price_level': 4,
            'type': 'nature',
            'rating': 4.9,
            'latitude': -18.2871,
            'longitude': 147.6992
        },
        {
            'name': 'Yellowstone National Park',
            'city': 'Wyoming',
            'country': 'USA',
            'description': 'Famous for its wildlife and geothermal features like Old Faithful.',
            'price_level': 2,
            'type': 'nature',
            'rating': 4.8,
            'latitude': 44.4280,
            'longitude': -110.5885
        },
        {
            'name': 'Victoria Falls',
            'city': 'Livingstone',
            'country': 'Zambia/Zimbabwe',
            'description': 'One of the largest waterfalls in the world.',
            'price_level': 3,
            'type': 'nature',
            'rating': 4.9,
            'latitude': -17.9243,
            'longitude': 25.8572
        },
        {
            'name': 'Santorini',
            'city': 'Cyclades',
            'country': 'Greece',
            'description': 'Known for its white-washed houses with blue domes overlooking the sea.',
            'price_level': 4,
            'type': 'nature',
            'rating': 4.7,
            'latitude': 36.3932,
            'longitude': 25.4615
        },
        
        # More Recreational locations
        {
            'name': 'Tokyo Disneyland',
            'city': 'Tokyo',
            'country': 'Japan',
            'description': 'The first Disney park outside the United States.',
            'price_level': 4,
            'type': 'recreational',
            'rating': 4.6,
            'latitude': 35.6329,
            'longitude': 139.8804
        },
        {
            'name': 'Copacabana Beach',
            'city': 'Rio de Janeiro',
            'country': 'Brazil',
            'description': 'Famous beach known for its white sand and lively atmosphere.',
            'price_level': 2,
            'type': 'recreational',
            'rating': 4.5,
            'latitude': -22.9868,
            'longitude': -43.1896
        },
        {
            'name': 'Dubai Miracle Garden',
            'city': 'Dubai',
            'country': 'UAE',
            'description': 'The world\'s largest natural flower garden with over 50 million flowers.',
            'price_level': 3,
            'type': 'recreational',
            'rating': 4.4,
            'latitude': 25.0661,
            'longitude': 55.2428
        },
        {
            'name': 'Eden Project',
            'city': 'Cornwall',
            'country': 'UK',
            'description': 'Huge biomes housing plant species from around the world.',
            'price_level': 3,
            'type': 'recreational',
            'rating': 4.5,
            'latitude': 50.3601,
            'longitude': -4.7447
        },
        
        # More Nightlife locations
        {
            'name': 'Club Space',
            'city': 'Miami',
            'country': 'USA',
            'description': 'Iconic club known for its marathon DJ sets and terrace.',
            'price_level': 4,
            'type': 'nightlife',
            'rating': 4.5,
            'latitude': 25.7860,
            'longitude': -80.1954
        },
        {
            'name': 'Ushuaïa',
            'city': 'Ibiza',
            'country': 'Spain',
            'description': 'Famous open-air club with pool parties and world-class DJs.',
            'price_level': 5,
            'type': 'nightlife',
            'rating': 4.7,
            'latitude': 38.8839,
            'longitude': 1.4096
        },
        {
            'name': 'KU DE TA',
            'city': 'Bali',
            'country': 'Indonesia',
            'description': 'Beach club with spectacular sunset views over the ocean.',
            'price_level': 4,
            'type': 'nightlife',
            'rating': 4.6,
            'latitude': -8.6785,
            'longitude': 115.1569
        },
        {
            'name': 'Tresor',
            'city': 'Berlin',
            'country': 'Germany',
            'description': 'Historic techno club set in a former power plant.',
            'price_level': 2,
            'type': 'nightlife',
            'rating': 4.6,
            'latitude': 52.5110,
            'longitude': 13.4186
        },
        
        # More Culture locations
        {
            'name': 'Machu Picchu',
            'city': 'Cusco Region',
            'country': 'Peru',
            'description': 'Ancient Incan citadel set high in the Andes Mountains.',
            'price_level': 4,
            'type': 'culture',
            'rating': 4.9,
            'latitude': -13.1631,
            'longitude': -72.5450
        },
        {
            'name': 'Taj Mahal',
            'city': 'Agra',
            'country': 'India',
            'description': 'Iconic marble mausoleum and UNESCO World Heritage Site.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.8,
            'latitude': 27.1751,
            'longitude': 78.0421
        },
        {
            'name': 'Forbidden City',
            'city': 'Beijing',
            'country': 'China',
            'description': 'Imperial palace complex from the Ming dynasty to the Qing dynasty.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.7,
            'latitude': 39.9163,
            'longitude': 116.3972
        },
        {
            'name': 'Vatican Museums',
            'city': 'Vatican City',
            'country': 'Vatican City',
            'description': 'Museums featuring some of the world\'s most important art collections.',
            'price_level': 3,
            'type': 'culture',
            'rating': 4.7,
            'latitude': 41.9064,
            'longitude': 12.4534
        },
        
        # More Food locations
        {
            'name': 'La Boqueria Market',
            'city': 'Barcelona',
            'country': 'Spain',
            'description': 'Famous public market with fresh food, tapas bars, and restaurants.',
            'price_level': 2,
            'type': 'food',
            'rating': 4.7,
            'latitude': 41.3818,
            'longitude': 2.1724
        },
        {
            'name': 'Noma',
            'city': 'Copenhagen',
            'country': 'Denmark',
            'description': 'Award-winning restaurant known for its reinvention of Nordic cuisine.',
            'price_level': 5,
            'type': 'food',
            'rating': 4.9,
            'latitude': 55.6833,
            'longitude': 12.6103
        },
        {
            'name': 'Katz\'s Delicatessen',
            'city': 'New York',
            'country': 'USA',
            'description': 'Iconic deli famous for its pastrami sandwiches.',
            'price_level': 3,
            'type': 'food',
            'rating': 4.5,
            'latitude': 40.7223,
            'longitude': -73.9874
        },
        {
            'name': 'Tsukiji Outer Market',
            'city': 'Tokyo',
            'country': 'Japan',
            'description': 'Famous market with hundreds of shops selling fresh seafood and produce.',
            'price_level': 3,
            'type': 'food',
            'rating': 4.6,
            'latitude': 35.6654,
            'longitude': 139.7707
        },
        {
            'name': 'Lake Baikal',
            'city': 'Siberia',
            'country': 'Russia',
            'description': 'The deepest and oldest lake in the world containing 20% of world\'s unfrozen freshwater.',
            'price_level': 3,
            'type': 'nature',
            'rating': 4.9,
            'latitude': 53.5587,
            'longitude': 108.1650
        },
        {
            'name': 'Bryce Canyon',
            'city': 'Utah',
            'country': 'USA',
            'description': 'Famous for its unique geology of red rock spires called hoodoos.',
            'price_level': 2,
            'type': 'nature',
            'rating': 4.8,
            'latitude': 37.6283,
            'longitude': -112.1676
        },
        {
            'name': 'Plitvice Lakes',
            'city': 'Lika-Senj County',
            'country': 'Croatia',
            'description': 'Cascading lakes known for their distinctive colors and waterfalls.',
            'price_level': 2,
            'type': 'nature',
            'rating': 4.9,
            'latitude': 44.8654,
            'longitude': 15.5820
        },

        # More Recreational locations
        {
            'name': 'Gardens by the Bay',
            'city': 'Singapore',
            'country': 'Singapore',
            'description': 'Futuristic park featuring massive Supertrees and stunning conservatories.',
            'price_level': 3,
            'type': 'recreational',
            'rating': 4.7,
            'latitude': 1.2816,
            'longitude': 103.8636
        },
        {
            'name': 'Bora Bora Lagoon',
            'city': 'Bora Bora',
            'country': 'French Polynesia',
            'description': 'Iconic turquoise lagoon with luxury overwater bungalows and coral reefs.',
            'price_level': 5,
            'type': 'recreational',
            'rating': 4.9,
            'latitude': -16.5004,
            'longitude': -151.7415
        },
        {
            'name': 'Blue Lagoon',
            'city': 'Grindavík',
            'country': 'Iceland',
            'description': 'Geothermal spa with mineral-rich waters known for relaxation and skin benefits.',
            'price_level': 4,
            'type': 'recreational',
            'rating': 4.6,
            'latitude': 63.8804,
            'longitude': -22.4495
        },

        # More Nightlife locations
        {
            'name': 'Mykonos Nightlife District',
            'city': 'Mykonos',
            'country': 'Greece',
            'description': 'Famous island featuring numerous bars, clubs, and beach parties.',
            'price_level': 4,
            'type': 'nightlife',
            'rating': 4.7,
            'latitude': 37.4467,
            'longitude': 25.3289
        },
        {
            'name': 'Lan Kwai Fong',
            'city': 'Hong Kong',
            'country': 'China',
            'description': 'Popular nightlife district with over 90 restaurants and bars.',
            'price_level': 4,
            'type': 'nightlife',
            'rating': 4.5,
            'latitude': 22.2808,
            'longitude': 114.1551
        },
        {
            'name': 'Shibuya Crossing',
            'city': 'Tokyo',
            'country': 'Japan',
            'description': 'Iconic intersection surrounded by neon lights, shopping, and nightlife.',
            'price_level': 3,
            'type': 'nightlife',
            'rating': 4.7,
            'latitude': 35.6594,
            'longitude': 139.7005
        },

        # More Culture locations
        {
            'name': 'Petra',
            'city': 'Ma\'an Governorate',
            'country': 'Jordan',
            'description': 'Ancient city carved into rose-colored stone, one of the New Seven Wonders of the World.',
            'price_level': 3,
            'type': 'culture',
            'rating': 4.9,
            'latitude': 30.3285,
            'longitude': 35.4444
        },
        {
            'name': 'Angkor Wat',
            'city': 'Siem Reap',
            'country': 'Cambodia',
            'description': 'Largest religious monument in the world, originally constructed as a Hindu temple.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.9,
            'latitude': 13.4125,
            'longitude': 103.8670
        },
        {
            'name': 'Chichen Itza',
            'city': 'Yucatan',
            'country': 'Mexico',
            'description': 'Large pre-Columbian archaeological site built by the Maya civilization.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.8,
            'latitude': 20.6843,
            'longitude': -88.5677
        },

        # More Food locations
        {
            'name': 'Tsukiji Outer Market',
            'city': 'Tokyo',
            'country': 'Japan',
            'description': 'Historic marketplace offering fresh seafood, produce, and kitchen tools.',
            'price_level': 3,
            'type': 'food',
            'rating': 4.7,
            'latitude': 35.6654,
            'longitude': 139.7707
        },
        {
            'name': 'Mercado de San Miguel',
            'city': 'Madrid',
            'country': 'Spain',
            'description': 'Covered market filled with tapas bars and gourmet food vendors.',
            'price_level': 3,
            'type': 'food',
            'rating': 4.6,
            'latitude': 40.4153,
            'longitude': -3.7089
        },
        {
            'name': 'Marrakech Medina Food Markets',
            'city': 'Marrakech',
            'country': 'Morocco',
            'description': 'Vibrant markets offering traditional Moroccan cuisine, spices, and street food.',
            'price_level': 2,
            'type': 'food',
            'rating': 4.7,
            'latitude': 31.6295,
            'longitude': -7.9811
        }
    ]
    
    all_locations = locations + additional_locations
    
    for loc_data in all_locations:
        # Check if this location already exists
        existing = Location.query.filter_by(
            name=loc_data['name'],
            city=loc_data['city'],
            country=loc_data['country']
        ).first()
        
        if not existing:
            # Only add if it doesn't exist
            print(f"Adding new location: {loc_data['name']}")
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
    
    # Add visits for other location types as well
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)