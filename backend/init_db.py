from app import create_app
from models import db, Location, User
from app import seed_locations, create_demo_user

print("Starting database initialization...")
app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("Tables created successfully.")
    
    # Check if locations exist
    location_count = Location.query.count()
    print(f"Found {location_count} existing locations.")
    
    if location_count == 0:
        print("Seeding locations...")
        seed_locations()
        new_location_count = Location.query.count()
        print(f"Seeded {new_location_count} locations.")
    
    # Check if demo user exists
    demo_user = User.query.filter_by(username='demouser').first()
    if not demo_user:
        print("Creating demo user...")
        create_demo_user()
        print("Demo user created successfully.")
    else:
        print("Demo user already exists.")
    
    # Verify locations and user
    final_location_count = Location.query.count()
    final_user_count = User.query.count()
    print(f"Final database state: {final_location_count} locations, {final_user_count} users")
    
    if final_location_count == 0:
        print("WARNING: No locations found after initialization!")
    else:
        print("Database initialized successfully.")