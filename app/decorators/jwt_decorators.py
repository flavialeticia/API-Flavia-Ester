from functools import wraps
from flask import request, jsonify, g
from jwt import ExpiredSignatureError, InvalidTokenError
from ..utils.jwt_utils import decode_token
from ..models.user import User

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token de autenticação ausente'}), 401
        token = auth_header.split(' ')[1]

        try:
            payload = decode_token(token)
            if payload['type'] != 'access':
                raise InvalidTokenError("Token inválido")

            user = User.query.get(payload['sub'])
            if not user:
                return jsonify({'error': 'Usuário não encontrado'}), 401

            g.current_user = user
            return f(*args, **kwargs)

        except ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        except Exception:
            return jsonify({'error': 'Erro de autenticação'}), 500

    return decorated

def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user = getattr(g, 'current_user', None)
            if user and user.perfil in roles:
                return f(*args, **kwargs)
            return jsonify({'error': 'Acesso negado'}), 403
        return wrapped
    return decorator
