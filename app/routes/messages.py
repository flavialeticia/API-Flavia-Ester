from flask import Blueprint, request
from ..models.message import Message
from .. import db
from ..schemas.message_schema import MessageSchema

messages_bp = Blueprint('messages', __name__)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

@messages_bp.route('/', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return messages_schema.jsonify(messages), 200

@messages_bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = Message.query.get_or_404(message_id)
    return message_schema.jsonify(message), 200

@messages_bp.route('/', methods=['POST'])
def create_message():
    data = request.get_json()
    message = Message(
        content=data['content'],
        user_id=1  # Usuário padrão
    )
    db.session.add(message)
    db.session.commit()
    return message_schema.jsonify(message), 201

@messages_bp.route('/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    message = Message.query.get_or_404(message_id)
    data = request.get_json()

    if 'content' in data:
        message.content = data['content']
    # Não permitimos alterar o user_id após a criação
    
    db.session.commit()
    return message_schema.jsonify(message), 200

@messages_bp.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return '', 204