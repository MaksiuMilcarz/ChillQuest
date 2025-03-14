from app import create_app
from models import db, Location
from app import seed_locations, create_demo_user
app = create_app()
with app.app_context():
    db.create_all()
    print("Tables created.")
    if Location.query.count() == 0:
        seed_locations()
        print("Locations seeded.")
    create_demo_user()
    print("Demo user created.")

