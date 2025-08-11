from flask import Blueprint, request, jsonify, g
from ..models.user import User
from .. import db
from ..schemas.user_schema import UserSchema
from marshmallow import ValidationError
from ..decorators.jwt_decorators import jwt_required, require_role

users_bp = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_bp.route('/', methods=['GET'])
@jwt_required
@require_role('ADMIN')
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required
def get_user(user_id):
    if g.current_user.id != user_id and g.current_user.perfil != 'ADMIN':
        return jsonify({'error': 'Acesso negado'}), 403

    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user)), 200

@users_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email já está em uso"}), 400

        # Se perfil for enviado e não for ADMIN, forçar USER
        if 'perfil' in data and (not hasattr(g, 'current_user') or g.current_user.perfil != 'ADMIN'):
            data['perfil'] = 'USER'

        user = User(
            email=data['email'],
            nome=data['nome'],
            senha=data['senha'],
            perfil=data.get('perfil', 'USER')
        )

        db.session.add(user)
        db.session.commit()
        return jsonify(user_schema.dump(user)), 201

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except KeyError as err:
        return jsonify({"error": f"Campo obrigatório faltando: {str(err)}"}), 400

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required
def update_user(user_id):
    if g.current_user.id != user_id and g.current_user.perfil != 'ADMIN':
        return jsonify({'error': 'Acesso negado'}), 403

    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if 'nome' in data:
        user.nome = data['nome']
    if 'email' in data:
        if User.query.filter(User.id != user_id, User.email == data['email']).first():
            return jsonify({"error": "Email já está em uso"}), 400
        user.email = data['email']
    if 'senha' in data:
        user.senha = data['senha']
    if 'perfil' in data and g.current_user.perfil == 'ADMIN':
        user.perfil = data['perfil']

    db.session.commit()
    return jsonify(user_schema.dump(user)), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required
@require_role('ADMIN')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
