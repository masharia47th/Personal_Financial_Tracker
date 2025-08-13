# app/services/auth.py
from flask import current_app
from app.models.user import User
from app import db
import jwt
import datetime

class AuthService:
    @staticmethod
    def register(username, password, currency='USD'):
        if User.query.filter_by(username=username).first():
            return None, 'Username already exists'
        user = User(username=username, currency=currency)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user, None

    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = jwt.encode({
                'user_id': str(user.id),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, current_app.config['SECRET_KEY'], algorithm='HS256')
            refresh_token = jwt.encode({
                'user_id': str(user.id),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
            }, current_app.config['SECRET_KEY'], algorithm='HS256')
            return access_token, refresh_token, None
        return None, None, 'Invalid credentials'

    @staticmethod
    def refresh(refresh_token):
        try:
            data = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.get(data['user_id'])
            if user:
                access_token = jwt.encode({
                    'user_id': str(user.id),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }, current_app.config['SECRET_KEY'], algorithm='HS256')
                return access_token, None
            return None, 'Invalid user'
        except jwt.ExpiredSignatureError:
            return None, 'Refresh token expired'
        except jwt.InvalidTokenError:
            return None, 'Invalid refresh token'

