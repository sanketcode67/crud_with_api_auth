from flask import Blueprint, jsonify, request,current_app
import jwt
from app import db
from app.models import User

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    # get the given user data from db
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # it means it is valid user so create JWT token
        token_payload = {'username': data['username']}
        access_token = jwt.encode(token_payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')   

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"message": "Username is already taken"}), 409

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201    