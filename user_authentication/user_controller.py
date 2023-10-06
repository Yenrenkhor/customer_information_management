from flask import Blueprint, request, jsonify
from .user_model import user_db, User
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash

# , jwt_refresh_token_required

user_auth_blueprint = Blueprint('user', __name__)


@user_auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Conflict", "message": "Username already exists"}), 409

    # Encrypt the password before storing it in the database
    hashed_password = generate_password_hash(password, method='sha256')

    new_user = User(username=username, password=hashed_password)
    user_db.session.add(new_user)
    user_db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201
    pass


@user_auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized", "message": "Invalid credentials"}), 401

    # Create JWT tokens for the authenticated user
    access_token = create_access_token(identity=user.username)
    refresh_token = create_refresh_token(identity=user.username)

    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
