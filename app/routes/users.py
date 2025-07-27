from flask import Blueprint, request, jsonify, g
from ..models.user import User
from .. import db
from ..schemas.user_schema import UserSchema
from marshmallow import ValidationError
from ..decorators.jwt_decorators import jwt_required, require_role

users_bp = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# GET /users — somente ADMIN pode listar todos os usuários
@users_bp.route('/', methods=['GET'])
@jwt_required
@require_role('ADMIN')
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

# GET /users/<id> — usuário pode acessar seus dados ou ADMIN pode acessar qualquer
@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required
def get_user(user_id):
    if g.current_user.id != user_id and g.current_user.perfil != 'ADMIN':
        return jsonify({'error': 'Acesso não autorizado'}), 403

    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user)), 200

# POST /users — criação pública de usuários (registro)
@users_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email já está em uso"}), 400

        user = User(
            email=data['email'],
            nome=data['nome'],
            senha=data['senha']  # o setter já faz o hash
        )
        # Por padrão perfil = 'USER' (definido no model)

        db.session.add(user)
        db.session.commit()
        return jsonify(user_schema.dump(user)), 201

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except KeyError as err:
        return jsonify({"error": f"Campo obrigatório faltando: {str(err)}"}), 400

# PUT /users/<id> — só o próprio usuário ou ADMIN podem editar
@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required
def update_user(user_id):
    if g.current_user.id != user_id and g.current_user.perfil != 'ADMIN':
        return jsonify({'error': 'Apenas o próprio usuário ou um administrador pode editar'}), 403

    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if 'nome' in data:
        user.nome = data['nome']
    if 'email' in data:
        # Verifica se email está em uso por outro usuário
        if User.query.filter(User.id != user_id, User.email == data['email']).first():
            return jsonify({"error": "Email já está em uso"}), 400
        user.email = data['email']
    if 'senha' in data:
        user.senha = data['senha']

    db.session.commit()
    return jsonify(user_schema.dump(user)), 200

# DELETE /users/<id> — somente ADMIN pode deletar usuários
@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required
@require_role('ADMIN')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
