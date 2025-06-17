from flask import Blueprint, request, jsonify
from ..models.user import User
from .. import db
from ..schemas.user_schema import UserSchema

users_bp = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    users_json = [user.to_dict() for user in users]
    return jsonify(users_json)

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user), 200

@users_bp.route('/', methods=['POST'])
def create_user():
    data = user_schema.load(request.get_json())
    db.session.add(data)
    db.session.commit()
    return user_schema.jsonify(data), 201

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = user_schema.load(request.get_json(), partial=True)

    db.session.commit()
    return user_schema.jsonify(data), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204