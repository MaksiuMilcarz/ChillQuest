# backend/seed_data.py
from app import create_app
from models import db, User, Location, Visit
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def seed_all_data():
    """Master function to seed all data for the application"""
    print("Starting comprehensive data seeding...")
    app = create_app()
    
    with app.app_context():
        # Check if we need to seed the database
        location_count = Location.query.count()
        print(f"Current location count: {location_count}")
        
        # Seed all locations
        seed_all_locations()
        
        # Create demo user with visits
        create_demo_user()
        
        # Print final state
        final_location_count = Location.query.count()
        final_user_count = User.query.count()
        final_visit_count = Visit.query.count()
        
        print(f"Database seeding complete!")
        print(f"- {final_location_count} total locations")
        print(f"- {final_user_count} users")
        print(f"- {final_visit_count} total visits")

def seed_all_locations():
    """Seed all locations (original + additional)"""
    print("Seeding all locations...")
    
    # Original locations from the app
    original_locations = [
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
        },
        # Additional locations from the original seed
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
    
    # Additional 100+ European locations (with some global gems)
    new_european_locations = [
        # EUROPEAN DESTINATIONS - Nature
        {
            'name': 'Lofoten Islands',
            'city': 'Nordland',
            'country': 'Norway',
            'description': 'Dramatic mountains, crystal-clear fjords, and picturesque fishing villages above the Arctic Circle.',
            'price_level': 4,
            'type': 'nature',
            'rating': 4.9,
            'latitude': 68.1557,
            'longitude': 13.6082
        },
        {
            'name': 'Cinque Terre',
            'city': 'Liguria',
            'country': 'Italy',
            'description': 'Five colorful coastal villages perched on steep cliffs overlooking the Mediterranean.',
            'price_level': 3,
            'type': 'nature',
            'rating': 4.8,
            'latitude': 44.1280,
            'longitude': 9.7230
        },
        {
            'name': 'Lake Como',
            'city': 'Lombardy',
            'country': 'Italy',
            'description': 'Y-shaped alpine lake surrounded by luxury villas and lush mountains.',
            'price_level': 4,
            'type': 'nature',
            'rating': 4.8,
            'latitude': 46.0160,
            'longitude': 9.2553
        },
        {
            'name': 'Faroe Islands',
            'city': 'Tórshavn',
            'country': 'Denmark',
            'description': 'Remote archipelago featuring dramatic landscapes, waterfalls, and puffins.',
            'price_level': 4,
            'type': 'nature',
            'rating': 4.9,
            'latitude': 62.0084,
            'longitude': -6.7768
        },
        {
            'name': 'Bavarian Alps',
            'city': 'Bavaria',
            'country': 'Germany',
            'description': 'Alpine mountains with picturesque villages, lakes and the famous Neuschwanstein Castle.',
            'price_level': 3,
            'type': 'nature',
            'rating': 4.7,
            'latitude': 47.5622,
            'longitude': 11.3540
        },
        {
            'name': 'Giant\'s Causeway',
            'city': 'County Antrim',
            'country': 'Northern Ireland',
            'description': 'Unique landscape of 40,000 interlocking basalt columns from ancient volcanic eruptions.',
            'price_level': 2,
            'type': 'nature',
            'rating': 4.8,
            'latitude': 55.2408,
            'longitude': -6.5115
        },
        {
            'name': 'Cappadocia',
            'city': 'Nevşehir',
            'country': 'Turkey',
            'description': 'Unique landscape with "fairy chimneys" rock formations and hot air balloon flights.',
            'price_level': 3,
            'type': 'nature',
            'rating': 4.8,
            'latitude': 38.6470,
            'longitude': 34.8424
        },
        {
            'name': 'Picos de Europa',
            'city': 'Asturias',
            'country': 'Spain',
            'description': 'Stunning limestone mountain range with hiking trails and breathtaking views.',
            'price_level': 2,
            'type': 'nature',
            'rating': 4.7,
            'latitude': 43.1968,
            'longitude': -4.8038
        },
        {
            'name': 'Meteora',
            'city': 'Kalabaka',
            'country': 'Greece',
            'description': 'Dramatic monasteries perched atop massive rock formations.',
            'price_level': 2,
            'type': 'nature',
            'rating': 4.9,
            'latitude': 39.7217,
            'longitude': 21.6306
        },
        {
            'name': 'Lake Bled',
            'city': 'Bled',
            'country': 'Slovenia',
            'description': 'Fairy-tale lake with an island church, medieval castle, and mountain backdrop.',
            'price_level': 2,
            'type': 'nature',
            'rating': 4.8,
            'latitude': 46.3639,
            'longitude': 14.0938
        },
        
        # EUROPEAN DESTINATIONS - Recreational
        {
            'name': 'Disneyland Paris',
            'city': 'Marne-la-Vallée',
            'country': 'France',
            'description': 'Disney\'s European theme park resort with two parks and entertainment district.',
            'price_level': 4,
            'type': 'recreational',
            'rating': 4.5,
            'latitude': 48.8716,
            'longitude': 2.7766
        },
        {
            'name': 'La Sagrada Familia',
            'city': 'Barcelona',
            'country': 'Spain',
            'description': 'Antoni Gaudí\'s iconic unfinished church with stunning architecture.',
            'price_level': 3,
            'type': 'recreational',
            'rating': 4.8,
            'latitude': 41.4036,
            'longitude': 2.1744
        },
        {
            'name': 'Park Güell',
            'city': 'Barcelona',
            'country': 'Spain',
            'description': 'Colorful park with amazing buildings, sculptures, and tile work designed by Gaudí.',
            'price_level': 2,
            'type': 'recreational',
            'rating': 4.7,
            'latitude': 41.4145,
            'longitude': 2.1527
        },
        {
            'name': 'Efteling',
            'city': 'Kaatsheuvel',
            'country': 'Netherlands',
            'description': 'One of Europe\'s oldest and most beloved fantasy-themed amusement parks.',
            'price_level': 3,
            'type': 'recreational',
            'rating': 4.8,
            'latitude': 51.6454,
            'longitude': 5.0431
        },
        {
            'name': 'Tivoli Gardens',
            'city': 'Copenhagen',
            'country': 'Denmark',
            'description': 'Historic amusement park with rides, games, and beautiful gardens.',
            'price_level': 3,
            'type': 'recreational',
            'rating': 4.7,
            'latitude': 55.6736,
            'longitude': 12.5681
        },
        {
            'name': 'PortAventura World',
            'city': 'Salou',
            'country': 'Spain',
            'description': 'Resort with three theme parks including Ferrari Land and Caribbean-themed water park.',
            'price_level': 4,
            'type': 'recreational',
            'rating': 4.6,
            'latitude': 41.0877,
            'longitude': 1.1567
        },
        {
            'name': 'Zugspitze',
            'city': 'Garmisch-Partenkirchen',
            'country': 'Germany',
            'description': 'Germany\'s highest peak with skiing, hiking, and panoramic views.',
            'price_level': 3,
            'type': 'recreational',
            'rating': 4.8,
            'latitude': 47.4208,
            'longitude': 10.9853
        },
        {
            'name': 'French Riviera',
            'city': 'Nice',
            'country': 'France',
            'description': 'Mediterranean coastline known for beaches, yachting, and luxury lifestyle.',
            'price_level': 5,
            'type': 'recreational',
            'rating': 4.7,
            'latitude': 43.7102,
            'longitude': 7.2620
        },
        {
            'name': 'Legoland Billund',
            'city': 'Billund',
            'country': 'Denmark',
            'description': 'Original Legoland park with miniature cities built from Lego bricks.',
            'price_level': 3,
            'type': 'recreational',
            'rating': 4.6,
            'latitude': 55.7350,
            'longitude': 9.1249
        },
        {
            'name': 'Chamonix-Mont-Blanc',
            'city': 'Chamonix',
            'country': 'France',
            'description': 'Alpine resort town with access to Mont Blanc and world-class skiing.',
            'price_level': 4,
            'type': 'recreational',
            'rating': 4.8,
            'latitude': 45.9237,
            'longitude': 6.8694
        },
        
        # EUROPEAN DESTINATIONS - Nightlife
        {
            'name': 'Amnesia',
            'city': 'Ibiza',
            'country': 'Spain',
            'description': 'Legendary nightclub with two massive rooms and foam parties.',
            'price_level': 5,
            'type': 'nightlife',
            'rating': 4.6,
            'latitude': 38.9513,
            'longitude': 1.4091
        },
        {
            'name': 'Soho District',
            'city': 'London',
            'country': 'UK',
            'description': 'Entertainment district with theaters, bars, clubs and restaurants.',
            'price_level': 4,
            'type': 'nightlife',
            'rating': 4.5,
            'latitude': 51.5133,
            'longitude': -0.1367
        },
        {
            'name': 'Ruin Bars',
            'city': 'Budapest',
            'country': 'Hungary',
            'description': 'Unique bars set in abandoned buildings with eclectic decor.',
            'price_level': 2,
            'type': 'nightlife',
            'rating': 4.7,
            'latitude': 47.4979,
            'longitude': 19.0606
        },
        {
            'name': 'Elrow',
            'city': 'Barcelona',
            'country': 'Spain',
            'description': 'Famous for its flamboyant parties with immersive themes and confetti cannons.',
            'price_level': 4,
            'type': 'nightlife',
            'rating': 4.8,
            'latitude': 41.3851,
            'longitude': 2.1734
        },
        {
            'name': 'Pag Island',
            'city': 'Novalja',
            'country': 'Croatia',
            'description': 'Croatia\'s party island with beach clubs and the famous Zrće Beach.',
            'price_level': 3,
            'type': 'nightlife',
            'rating': 4.5,
            'latitude': 44.5579,
            'longitude': 14.8725
        },
        {
            'name': 'Temple Bar',
            'city': 'Dublin',
            'country': 'Ireland',
            'description': 'Cultural quarter with medieval streets, pubs, and live music.',
            'price_level': 3,
            'type': 'nightlife',
            'rating': 4.4,
            'latitude': 53.3453,
            'longitude': -6.2646
        },
        {
            'name': 'Reeperbahn',
            'city': 'Hamburg',
            'country': 'Germany',
            'description': 'Famous entertainment district with clubs, bars, and theaters.',
            'price_level': 3,
            'type': 'nightlife',
            'rating': 4.4,
            'latitude': 53.5496,
            'longitude': 9.9646
        },
        {
            'name': 'Hvar Town',
            'city': 'Hvar',
            'country': 'Croatia',
            'description': 'Trendy island destination with beach clubs, bars, and yacht parties.',
            'price_level': 4,
            'type': 'nightlife',
            'rating': 4.6,
            'latitude': 43.1717,
            'longitude': 16.4417
        },
        {
            'name': 'DC10',
            'city': 'Ibiza',
            'country': 'Spain',
            'description': 'Underground club in a converted farmhouse known for techno and house music.',
            'price_level': 4,
            'type': 'nightlife',
            'rating': 4.7,
            'latitude': 38.8777,
            'longitude': 1.4067
        },
        {
            'name': 'Canal Street',
            'city': 'Manchester',
            'country': 'UK',
            'description': 'Famous LGBTQ+ district with bars, clubs, and restaurants.',
            'price_level': 3,
            'type': 'nightlife',
            'rating': 4.5,
            'latitude': 53.4770,
            'longitude': -2.2384
        },
        
        # EUROPEAN DESTINATIONS - Culture
        {
            'name': 'Prado Museum',
            'city': 'Madrid',
            'country': 'Spain',
            'description': 'Spain\'s national art museum with works by Goya, Velázquez, and El Greco.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.8,
            'latitude': 40.4138,
            'longitude': -3.6921
        },
        {
            'name': 'Alhambra',
            'city': 'Granada',
            'country': 'Spain',
            'description': 'Stunning palace and fortress complex from the Moorish period.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.9,
            'latitude': 37.1763,
            'longitude': -3.5886
        },
        {
            'name': 'Sagrada Familia',
            'city': 'Barcelona',
            'country': 'Spain',
            'description': 'Antoni Gaudí\'s unfinished masterpiece basilica with unique architecture.',
            'price_level': 3,
            'type': 'culture',
            'rating': 4.8,
            'latitude': 41.4036,
            'longitude': 2.1744
        },
        {
            'name': 'Colosseum',
            'city': 'Rome',
            'country': 'Italy',
            'description': 'Iconic ancient Roman amphitheater and UNESCO World Heritage site.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.8,
            'latitude': 41.8902,
            'longitude': 12.4922
        },
        {
            'name': 'Rijksmuseum',
            'city': 'Amsterdam',
            'country': 'Netherlands',
            'description': 'Dutch national museum dedicated to arts and history with works by Rembrandt.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.7,
            'latitude': 52.3600,
            'longitude': 4.8852
        },
        {
            'name': 'Palace of Versailles',
            'city': 'Versailles',
            'country': 'France',
            'description': 'Opulent royal château with stunning gardens and Hall of Mirrors.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.7,
            'latitude': 48.8049,
            'longitude': 2.1204
        },
        {
            'name': 'Neuschwanstein Castle',
            'city': 'Bavaria',
            'country': 'Germany',
            'description': 'Fairytale castle that inspired Disney\'s Sleeping Beauty Castle.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.8,
            'latitude': 47.5576,
            'longitude': 10.7498
        },
        {
            'name': 'Anne Frank House',
            'city': 'Amsterdam',
            'country': 'Netherlands',
            'description': 'Museum dedicated to Jewish wartime diarist Anne Frank.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.7,
            'latitude': 52.3752,
            'longitude': 4.8840
        },
        {
            'name': 'Uffizi Gallery',
            'city': 'Florence',
            'country': 'Italy',
            'description': 'Art museum with masterpieces from the Renaissance period.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.8,
            'latitude': 43.7677,
            'longitude': 11.2553
        },
        {
            'name': 'Edinburgh Castle',
            'city': 'Edinburgh',
            'country': 'UK',
            'description': 'Historic fortress dominating the skyline of Edinburgh.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.7,
            'latitude': 55.9486,
            'longitude': -3.1999
        },
        {
            'name': 'Musée d\'Orsay',
            'city': 'Paris',
            'country': 'France',
            'description': 'Museum in a former railway station housing impressionist masterpieces.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.8,
            'latitude': 48.8600,
            'longitude': 2.3266
        },
        {
            'name': 'Schönbrunn Palace',
            'city': 'Vienna',
            'country': 'Austria',
            'description': 'Former imperial summer residence with 1,441 rooms and beautiful gardens.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.7,
            'latitude': 48.1858,
            'longitude': 16.3122
        },
        {
            'name': 'Tower of London',
            'city': 'London',
            'country': 'UK',
            'description': 'Historic castle on the Thames housing the Crown Jewels.',
            'price_level': 3,
            'type': 'culture',
            'rating': 4.6,
            'latitude': 51.5081,
            'longitude': -0.0759
        },
        {
            'name': 'Sistine Chapel',
            'city': 'Vatican City',
            'country': 'Vatican City',
            'description': 'Chapel with ceiling painted by Michelangelo and site of papal conclaves.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.9,
            'latitude': 41.9029,
            'longitude': 12.4545
        },
        {
            'name': 'Guggenheim Museum Bilbao',
            'city': 'Bilbao',
            'country': 'Spain',
            'description': 'Frank Gehry-designed modern art museum with titanium exterior.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.7,
            'latitude': 43.2686,
            'longitude': -2.9340
        },
        
        # EUROPEAN DESTINATIONS - Food
        {
            'name': 'Mercado de San Miguel',
            'city': 'Madrid',
            'country': 'Spain',
            'description': 'Historic market with gourmet tapas, wine, and Spanish delicacies.',
            'price_level': 3,
            'type': 'food',
            'rating': 4.6,
            'latitude': 40.4153,
            'longitude': -3.7091
        },
        {
            'name': 'Osteria Francescana',
            'city': 'Modena',
            'country': 'Italy',
            'description': 'Three-Michelin-star restaurant by Chef Massimo Bottura.',
            'price_level': 5,
            'type': 'food',
            'rating': 4.9,
            'latitude': 44.6448,
            'longitude': 10.9281
        },
        {
            'name': 'Rialto Fish Market',
            'city': 'Venice',
            'country': 'Italy',
            'description': 'Historic fish market with fresh seafood and nearby cicchetti bars.',
            'price_level': 2,
            'type': 'food',
            'rating': 4.6,
            'latitude': 45.4408,
            'longitude': 12.3347
        },
        {
            'name': 'Borough Market',
            'city': 'London',
            'country': 'UK',
            'description': 'One of London\'s oldest food markets with artisanal products.',
            'price_level': 3,
            'type': 'food',
            'rating': 4.7,
            'latitude': 51.5055,
            'longitude': -0.0911
        },
        {
            'name': 'Boqueria Market',
            'city': 'Barcelona',
            'country': 'Spain',
            'description': 'Colorful public market with fresh produce, seafood, and tapas bars.',
            'price_level': 2,
            'type': 'food',
            'rating': 4.7,
            'latitude': 41.3817,
            'longitude': 2.1717
        },
        {
            'name': 'Pastéis de Belém',
            'city': 'Lisbon',
            'country': 'Portugal',
            'description': 'Home of the original Portuguese custard tarts since 1837.',
            'price_level': 2,
            'type': 'food',
            'rating': 4.8,
            'latitude': 38.6975,
            'longitude': -9.2037
        },
        {
            'name': 'Naschmarkt',
            'city': 'Vienna',
            'country': 'Austria',
            'description': 'Vienna\'s largest market with international food stalls and restaurants.',
            'price_level': 2,
            'type': 'food',
            'rating': 4.6,
            'latitude': 48.1996,
            'longitude': 16.3628
        },
        {
            'name': 'Café Central',
            'city': 'Vienna',
            'country': 'Austria',
            'description': 'Historic coffeehouse once frequented by Freud, Trotsky, and Lenin.',
            'price_level': 3,
            'type': 'food',
            'rating': 4.6,
            'latitude': 48.2102,
            'longitude': 16.3655
        },
        {
            'name': 'Geranium',
            'city': 'Copenhagen',
            'country': 'Denmark',
            'description': 'Three-Michelin-star restaurant serving elevated New Nordic cuisine.',
            'price_level': 5,
            'type': 'food',
            'rating': 4.9,
            'latitude': 55.7035,
            'longitude': 12.5743
        },
        {
            'name': 'Mercado da Ribeira',
            'city': 'Lisbon',
            'country': 'Portugal',
            'description': 'Time Out Market with top chefs and vendors in historic market hall.',
            'price_level': 3,
            'type': 'food',
            'rating': 4.7,
            'latitude': 38.7067,
            'longitude': -9.1458
        },
        {
            'name': 'Great Market Hall',
            'city': 'Budapest',
            'country': 'Hungary',
            'description': 'Largest indoor market in Budapest with traditional Hungarian foods.',
            'price_level': 2,
            'type': 'food',
            'rating': 4.5,
            'latitude': 47.4873,
            'longitude': 19.0587
        },
        {
            'name': 'Trattoria da Romano',
            'city': 'Burano',
            'country': 'Italy',
            'description': 'Historic restaurant on the colorful island of Burano known for risotto.',
            'price_level': 3,
            'type': 'food',
            'rating': 4.6,
            'latitude': 45.4859,
            'longitude': 12.4167
        },
        {
            'name': 'El Celler de Can Roca',
            'city': 'Girona',
            'country': 'Spain',
            'description': 'Three-Michelin-star restaurant run by the Roca brothers.',
            'price_level': 5,
            'type': 'food',
            'rating': 4.9,
            'latitude': 41.9886,
            'longitude': 2.8145
        },
        {
            'name': 'Les Halles de Lyon-Paul Bocuse',
            'city': 'Lyon',
            'country': 'France',
            'description': 'Indoor food market with gourmet vendors in France\'s gastronomic capital.',
            'price_level': 4,
            'type': 'food',
            'rating': 4.7,
            'latitude': 45.7629,
            'longitude': 4.8559
        },
        {
            'name': 'Café de Flore',
            'city': 'Paris',
            'country': 'France',
            'description': 'Historic café frequented by famous writers and philosophers.',
            'price_level': 3,
            'type': 'food',
            'rating': 4.4,
            'latitude': 48.8537,
            'longitude': 2.3335
        },
        
        # GLOBAL DESTINATIONS - Iconic Places
        {
            'name': 'Salar de Uyuni',
            'city': 'Uyuni',
            'country': 'Bolivia',
            'description': 'World\'s largest salt flat creating mirror effect during rainy season.',
            'price_level': 3,
            'type': 'nature',
            'rating': 4.9,
            'latitude': -20.1338,
            'longitude': -67.4891
        },
        {
            'name': 'Marina Bay Sands',
            'city': 'Singapore',
            'country': 'Singapore',
            'description': 'Iconic hotel with infinity pool overlooking the city skyline.',
            'price_level': 5,
            'type': 'recreational',
            'rating': 4.8,
            'latitude': 1.2834,
            'longitude': 103.8607
        },
        {
            'name': 'Table Mountain',
            'city': 'Cape Town',
            'country': 'South Africa',
            'description': 'Iconic flat-topped mountain overlooking Cape Town with cable car access.',
            'price_level': 2,
            'type': 'nature',
            'rating': 4.9,
            'latitude': -33.9628,
            'longitude': 18.4098
        },
        {
            'name': 'Dubai Mall',
            'city': 'Dubai',
            'country': 'UAE',
            'description': 'World\'s largest mall with shopping, aquarium, and indoor theme parks.',
            'price_level': 4,
            'type': 'recreational',
            'rating': 4.7,
            'latitude': 25.1972,
            'longitude': 55.2798
        },
        {
            'name': 'Burj Khalifa',
            'city': 'Dubai',
            'country': 'UAE',
            'description': 'World\'s tallest building with observation decks and restaurants.',
            'price_level': 4,
            'type': 'recreational',
            'rating': 4.7,
            'latitude': 25.1972,
            'longitude': 55.2744
        },
        {
            'name': 'Kyoto Imperial Palace',
            'city': 'Kyoto',
            'country': 'Japan',
            'description': 'Former residence of Japan\'s Imperial Family with beautiful gardens.',
            'price_level': 1,
            'type': 'culture',
            'rating': 4.6,
            'latitude': 35.0254,
            'longitude': 135.7621
        },
        {
            'name': 'Tsukiji Fish Market',
            'city': 'Tokyo',
            'country': 'Japan',
            'description': 'Largest wholesale fish and seafood market with early morning tuna auctions.',
            'price_level': 2,
            'type': 'food',
            'rating': 4.7,
            'latitude': 35.6654,
            'longitude': 139.7707
        },
        {
            'name': 'Christ the Redeemer',
            'city': 'Rio de Janeiro',
            'country': 'Brazil',
            'description': 'Iconic 30-meter statue of Jesus Christ overlooking Rio de Janeiro.',
            'price_level': 2,
            'type': 'culture',
            'rating': 4.8,
            'latitude': -22.9519,
            'longitude': -43.2106
        },
        {
            'name': 'Sydney Harbour Bridge',
            'city': 'Sydney',
            'country': 'Australia',
            'description': 'Iconic steel arch bridge with bridge climb experiences.',
            'price_level': 3,
            'type': 'recreational',
            'rating': 4.8,
            'latitude': -33.8523,
            'longitude': 151.2107
        },
        {
            'name': 'Golden Gate Bridge',
            'city': 'San Francisco',
            'country': 'USA',
            'description': 'Iconic suspension bridge spanning the Golden Gate Strait.',
            'price_level': 1,
            'type': 'recreational',
            'rating': 4.8,
            'latitude': 37.8199,
            'longitude': -122.4783
        }
    ]
    
    # Combine all locations
    all_locations = original_locations + new_european_locations
    
    # Add locations to database (only if they don't exist)
    added_count = 0
    for loc_data in all_locations:
        # Check if location already exists
        existing = Location.query.filter_by(
            name=loc_data['name'],
            city=loc_data['city'],
            country=loc_data['country']
        ).first()
        
        if not existing:
            location = Location(**loc_data)
            db.session.add(location)
            added_count += 1
            print(f"Adding new location: {loc_data['name']}")
    
    # Commit changes
    db.session.commit()
    
    # Final count
    final_count = Location.query.count()
    print(f"Added {added_count} new locations")
    print(f"Total locations in database: {final_count}")

def create_demo_user():
    """Create a demo user with predefined visits focused on nightlife"""
    # Check if demo user already exists
    if User.query.filter_by(username='demouser').first():
        print("Demo user already exists.")
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
    
    # Add a few visits to popular nature spots with lower ratings (not the demo user's preference)
    nature_locations = Location.query.filter_by(type='nature').limit(10).all()
    for location in nature_locations:
        days_ago = random.randint(50, 300)  # Less recent visits
        visit_date = now - timedelta(days=days_ago)
        
        # Assign a lower rating (not as enthusiastic about nature)
        rating = random.choice([3, 4])  # Doesn't enjoy nature as much
        
        notes = ""
        if rating == 3:
            notes = f"Nice place, but a bit too quiet for my taste. {location.name} was pretty though."
        elif rating == 4:
            notes = f"Beautiful scenery at {location.name}. Worth the trip!"
        
        visit = Visit(
            user_id=demo_user.id,
            location_id=location.id,
            visit_date=visit_date,
            rating=rating,
            notes=notes
        )
        db.session.add(visit)
    
    # Add visits to food locations with mixed ratings
    food_locations = Location.query.filter_by(type='food').limit(5).all()
    for location in food_locations:
        days_ago = random.randint(20, 150)
        visit_date = now - timedelta(days=days_ago)
        
        # Mixed ratings for food (some good, some not so good)
        rating = random.choice([3, 4, 5])
        
        notes = ""
        if rating == 5:
            notes = f"Amazing food at {location.name}! The flavors were incredible."
        elif rating == 4:
            notes = f"Good food at {location.name}. Would recommend."
        elif rating == 3:
            notes = f"Decent food at {location.name}, but nothing special."
        
        visit = Visit(
            user_id=demo_user.id,
            location_id=location.id,
            visit_date=visit_date,
            rating=rating,
            notes=notes
        )
        db.session.add(visit)
    
    # Add a few cultural visits
    culture_locations = Location.query.filter_by(type='culture').limit(5).all()
    for location in culture_locations:
        days_ago = random.randint(100, 400)
        visit_date = now - timedelta(days=days_ago)
        
        # Mixed ratings for culture (some interest, but not primary)
        rating = random.choice([3, 4])
        
        notes = f"Visited {location.name} with friends. Interesting place with rich history."
        
        visit = Visit(
            user_id=demo_user.id,
            location_id=location.id,
            visit_date=visit_date,
            rating=rating,
            notes=notes
        )
        db.session.add(visit)
    
    # Commit all the visits
    db.session.commit()
    print(f"Demo user created with {Location.query.filter_by(type='nightlife').count()} nightlife visits and some other location types.")

def reset_database():
    """Drop all tables and recreate them from scratch"""
    print("Resetting database completely...")
    app = create_app()
    
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("All tables dropped.")
        
        # Recreate tables
        db.create_all()
        print("Tables recreated.")
        
        # Seed data
        seed_all_data()

if __name__ == "__main__":
    # Call this for a normal seeding operation (no data loss)
    seed_all_data()
    
    # Uncomment to reset the entire database (WARNING: all data will be lost)
    reset_database()