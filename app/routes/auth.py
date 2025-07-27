from flask import Blueprint, request, jsonify, g
from ..models.user import User
from ..models.refreshtoken import RefreshToken
from .. import db
from ..utils.jwt_utils import create_access_token, create_refresh_token, decode_token
from werkzeug.exceptions import Unauthorized
from datetime import datetime
from jwt import ExpiredSignatureError, InvalidTokenError
from ..decorators.jwt_decorators import jwt_required

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


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    token_str = data.get('refresh_token')

    try:
        payload = decode_token(token_str)
        if payload['type'] != 'refresh':
            raise InvalidTokenError("Token inválido")

        token_db = RefreshToken.query.filter_by(token=token_str).first()
        if not token_db or token_db.expires_at < datetime.utcnow():
            raise Unauthorized("Refresh token expirado ou inválido")

        user = User.query.get(payload['sub'])
        if not user:
            raise Unauthorized("Usuário não encontrado")

        # Remover token antigo para evitar reuso
        db.session.delete(token_db)

        # Criar novo refresh token
        new_refresh_token_str, new_expires_at = create_refresh_token(user.id)
        new_refresh_token = RefreshToken(token=new_refresh_token_str, user_id=user.id, expires_at=new_expires_at)
        db.session.add(new_refresh_token)

        # Criar novo access token
        new_access_token = create_access_token(user.id, user.perfil)

        db.session.commit()

        return jsonify({
            'access_token': new_access_token,
            'refresh_token': new_refresh_token_str
        }), 200

    except ExpiredSignatureError:
        return jsonify({'error': 'Refresh token expirado'}), 401
    except (InvalidTokenError, Unauthorized) as e:
        return jsonify({'error': str(e)}), 401
    except Exception:
        return jsonify({'error': 'Erro ao renovar token'}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    user = g.current_user
    # Remover todos os refresh tokens do usuário
    RefreshToken.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    return jsonify({'message': 'Logout realizado com sucesso'}), 200

