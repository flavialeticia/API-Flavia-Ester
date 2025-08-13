from flask import Blueprint, request, jsonify, g
from ..models.message import Message
from .. import db
from ..schemas.message_schema import MessageSchema
from ..decorators.jwt_decorators import jwt_required, require_role

messages_bp = Blueprint('messages', __name__)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

@messages_bp.route('/', methods=['GET'])
def get_messages():
    messages = Message.query.filter_by(deleted=False).all()  # listar só não deletadas
    return jsonify(messages_schema.dump(messages)), 200

@messages_bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = Message.query.filter_by(id=message_id, deleted=False).first_or_404()
    return jsonify(message_schema.dump(message)), 200

@messages_bp.route('/', methods=['POST'])
@jwt_required
def create_message():
    data = request.get_json()
    
    if not data.get('titulo') or not data.get('conteudo'):
        return jsonify({"error": "titulo e conteudo são obrigatórios"}), 400

    message = Message(
        titulo=data['titulo'],
        conteudo=data['conteudo'],
        user_id=g.current_user.id,
        curtidas=0  # garante curtidas inicia 0
    )
    
    db.session.add(message)
    db.session.commit()
    return jsonify(message_schema.dump(message)), 201

@messages_bp.route('/<int:message_id>', methods=['PUT'])
@jwt_required
def update_message(message_id):
    message = Message.query.filter_by(id=message_id, deleted=False).first_or_404()
    
    if message.user_id != g.current_user.id and g.current_user.perfil != 'ADMIN':
        return jsonify({'error': 'Acesso negado'}), 403

    data = request.get_json()

    # Bloqueia alteração direta de 'curtidas'
    if 'curtidas' in data:
        return jsonify({'error': 'Campo "curtidas" não pode ser alterado diretamente'}), 422

    if 'titulo' in data:
        message.titulo = data['titulo']
    if 'conteudo' in data:
        message.conteudo = data['conteudo']

    db.session.commit()
    return jsonify(message_schema.dump(message)), 200

@messages_bp.route('/<int:message_id>', methods=['DELETE'])
@jwt_required
def delete_message(message_id):
    message = Message.query.filter_by(id=message_id, deleted=False).first_or_404()

    if message.user_id != g.current_user.id and g.current_user.perfil != 'ADMIN':
        return jsonify({'error': 'Acesso negado'}), 403

    # Soft delete
    message.deleted = True
    db.session.commit()
    return '', 204

@messages_bp.route('/<int:message_id>/curtir', methods=['POST'])
@jwt_required
def curtir_message(message_id):
    message = Message.query.filter_by(id=message_id, deleted=False).first_or_404()

    # Autor e admin não podem curtir
    if message.user_id == g.current_user.id or g.current_user.perfil == 'ADMIN':
        return jsonify({'error': 'Usuário não pode curtir esta mensagem'}), 403

    message.curtidas += 1
    db.session.commit()
    return jsonify(message_schema.dump(message)), 200

@messages_bp.route('/excluidas', methods=['GET'])
@jwt_required
def get_deleted_messages():
    if g.current_user.perfil != 'ADMIN':
        return jsonify({'error': 'Acesso negado'}), 403

    messages = Message.query.filter_by(deleted=True).all()
    return jsonify(messages_schema.dump(messages)), 200
