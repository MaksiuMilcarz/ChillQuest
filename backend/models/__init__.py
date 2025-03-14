from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# User model in the same file to avoid circular imports
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    visits = db.relationship('Visit', backref='user', lazy='dynamic')
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)
        print(f"Creating user {username} with password hash: {self.password_hash[:20]}...")
    
    def set_password(self, password):
        # Generate a password hash
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        # Debug password checking
        print(f"Checking password for {self.username}")
        print(f"Stored hash: {self.password_hash[:20]}...")
        result = check_password_hash(self.password_hash, password)
        print(f"Password check result: {result}")
        return result
    
    def __repr__(self):
        return f'<User {self.username}>'

# Location model
class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price_level = db.Column(db.Integer)  # 1-5 for price range
    type = db.Column(db.String(50))  # nature, recreational, nightlife, culture, food
    rating = db.Column(db.Float)  # Average rating (0-5)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Relationships
    visits = db.relationship('Visit', backref='location', lazy='dynamic')
    
    def __repr__(self):
        return f'<Location {self.name}, {self.city}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'country': self.country,
            'description': self.description,
            'price_level': self.price_level,
            'type': self.type,
            'rating': self.rating,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

# Visit model
class Visit(db.Model):
    __tablename__ = 'visits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    visit_date = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Integer)  # User's rating (1-5)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Visit User:{self.user_id} Location:{self.location_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'location_id': self.location_id,
            'visit_date': self.visit_date.isoformat(),
            'rating': self.rating,
            'notes': self.notes
        }