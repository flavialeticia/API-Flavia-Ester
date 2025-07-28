from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from flask import current_app
import jwt

def create_access_token(user_id, perfil):
    expire = datetime.utcnow() + timedelta(minutes=current_app.config['ACCESS_TOKEN_EXPIRES_MINUTES'])
    payload = {
        'sub': str(user_id),  # <-- Convertendo para string
        'perfil': perfil,
        'exp': expire,
        'type': 'access'
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def create_refresh_token(user_id):
    expire = datetime.utcnow() + timedelta(days=current_app.config['REFRESH_TOKEN_EXPIRES_DAYS'])
    payload = {
        'sub': str(user_id),  # <-- Convertendo para string
        'exp': expire,
        'type': 'refresh'
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token, expire


def decode_token(token):
    # Verifica expiração automaticamente
    return jwt.decode(
        token,
        current_app.config['SECRET_KEY'],
        algorithms=['HS256'],
        options={"verify_exp": True}
    )