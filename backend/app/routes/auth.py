# app/routes/auth.py
from flask import Blueprint, request, jsonify
from app.services.auth import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    currency = data.get('currency', 'USD')
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    user, error = AuthService.register(username, password, currency)
    if error:
        return jsonify({'error': error}), 400
    return jsonify({'user': user.to_dict()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    access_token, refresh_token, error = AuthService.login(username, password)
    if error:
        return jsonify({'error': error}), 401
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': User.query.filter_by(username=username).first().to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'Missing refresh token'}), 400
    access_token, error = AuthService.refresh(refresh_token)
    if error:
        return jsonify({'error': error}), 401
    return jsonify({'access_token': access_token}), 200

