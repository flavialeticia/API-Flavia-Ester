from flask import Blueprint, request, jsonify
from ..models.user import User
from ..models.refreshtoken import RefreshToken
from .. import db
from ..utils.jwt_utils import create_access_token, create_refresh_token
from werkzeug.exceptions import Unauthorized
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    user = User.query.filter_by(email=email).first()
    if not user or not user.verificar_senha(senha):
        raise Unauthorized('Email ou senha inválidos')

    access_token = create_access_token(user.id, user.perfil)
    refresh_token_str, expires_at = create_refresh_token(user.id)

    # Armazenar o refresh token no banco
    refresh_token = RefreshToken(token=refresh_token_str, user_id=user.id, expires_at=expires_at)
    db.session.add(refresh_token)
    db.session.commit()

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token_str
    }), 200
