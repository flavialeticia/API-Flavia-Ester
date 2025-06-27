from flask import Blueprint, request, jsonify # Adicionar jsonify
from ..models.message import Message
from .. import db
from ..schemas.message_schema import MessageSchema

messages_bp = Blueprint('messages', __name__)
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

@messages_bp.route('/', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    # Modificar para usar jsonify do Flask com dump do schema
    return jsonify(messages_schema.dump(messages)), 200

@messages_bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = Message.query.get_or_404(message_id)
    # Modificar para usar jsonify do Flask com dump do schema
    return jsonify(message_schema.dump(message)), 200

@messages_bp.route('/', methods=['POST'])
def create_message():
    data = request.get_json()
    message = Message(
        content=data['content'],
        user_id=1
    )
    db.session.add(message)
    db.session.commit()
    # Modificar para usar jsonify do Flask com dump do schema
    return jsonify(message_schema.dump(message)), 201

@messages_bp.route('/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    message = Message.query.get_or_404(message_id)
    data = request.get_json()

    if 'content' in data:
        message.content = data['content']
    
    db.session.commit()
    # Modificar para usar jsonify do Flask com dump do schema
    return jsonify(message_schema.dump(message)), 200

@messages_bp.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return '', 204
