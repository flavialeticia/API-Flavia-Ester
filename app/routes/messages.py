from flask import Blueprint, request, jsonify
from ..models.message import Message
from .. import db
from ..schemas.message_schema import MessageSchema
from ..decorators.jwt_decorators import jwt_required, require_role
from flask import g

messages_bp = Blueprint('messages', __name__)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

@messages_bp.route('/', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify(messages_schema.dump(messages)), 200

@messages_bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = Message.query.get_or_404(message_id)
    return jsonify(message_schema.dump(message)), 200

@messages_bp.route('/', methods=['POST'])
@jwt_required
def create_message():
    data = request.get_json()
    
    # Valide os campos obrigatórios
    if not data.get('titulo') or not data.get('conteudo'):
        return jsonify({"error": "titulo e conteudo são obrigatórios"}), 400

    message = Message(
        titulo=data['titulo'],  # Campo corrigido
        conteudo=data['conteudo'],  # Campo corrigido
        user_id=g.current_user.id
    )
    
    db.session.add(message)
    db.session.commit()
    return jsonify(message_schema.dump(message)), 201

@messages_bp.route('/<int:message_id>', methods=['PUT'])
@jwt_required
def update_message(message_id):
    message = Message.query.get_or_404(message_id)
    
    if message.user_id != g.current_user.id and g.current_user.perfil != 'ADMIN':
        return jsonify({'error': 'Acesso negado'}), 403

    data = request.get_json()
    
    # Atualize para os novos campos
    if 'titulo' in data:
        message.titulo = data['titulo']
    if 'conteudo' in data:
        message.conteudo = data['conteudo']

    db.session.commit()
    return jsonify(message_schema.dump(message)), 200

@messages_bp.route('/<int:message_id>', methods=['DELETE'])
@jwt_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    if message.user_id != g.current_user.id and g.current_user.perfil != 'ADMIN':
        return jsonify({'error': 'Acesso negado'}), 403
    db.session.delete(message)
    db.session.commit()
    return '', 204
