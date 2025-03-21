from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models import db, User
from . import auth_bp

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Debug for registration
    print(f"Registration attempt with username: {data.get('username', 'unknown')}")
    
    # Check if required fields are present
    if not all(k in data for k in ('username', 'email', 'password')):
        print("Missing required fields for registration")
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        print(f"Username already exists: {data['username']}")
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        print(f"Email already exists: {data['email']}")
        return jsonify({'message': 'Email already exists'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    db.session.add(user)
    db.session.commit()
    print(f"User registered successfully: {user.username}, ID: {user.id}")
    
    # Create access token - IMPORTANT: Convert user.id to string
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        },
        'access_token': access_token
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    print(f"Login request received: {data}")
    
    # Check if required fields are present
    if not all(k in data for k in ('username', 'password')):
        print("Missing required fields in login data")
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Find user
    user = User.query.filter_by(username=data['username']).first()
    
    # Debug user info
    if user:
        print(f"User found: {user.username}, ID: {user.id}")
        valid_password = user.check_password(data['password'])
        print(f"Password valid: {valid_password}")
    else:
        print(f"User not found: {data['username']}")
        all_users = User.query.all()
        print(f"Available users: {[u.username for u in all_users]}")
    
    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Create access token - IMPORTANT: Convert user.id to string
    access_token = create_access_token(identity=str(user.id))
    print(f"Login successful, token created for user: {user.username}")
    
    response = {
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        },
        'access_token': access_token
    }
    print(f"Sending response: {response}")
    
    return jsonify(response), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    # Get identity as string and convert to int if needed
    current_user_id = get_jwt_identity()
    try:
        user_id = int(current_user_id)
    except (ValueError, TypeError):
        user_id = current_user_id
        
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    }), 200

@auth_bp.route('/verify', methods=['GET'])
def verify_auth():
    auth_header = request.headers.get('Authorization', 'None')
    return jsonify({
        "message": "Auth headers received",
        "auth_header": auth_header,
        "all_headers": dict(request.headers)
    })