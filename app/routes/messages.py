from flask import Blueprint, request, jsonify, abort
from ..models.message import Message
from .. import db

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([msg.to_dict() for msg in messages]), 200

@messages_bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = Message.query.get_or_404(message_id)
    return jsonify(message.to_dict()), 200

@messages_bp.route('/', methods=['POST'])
def create_message():
    data = request.get_json()
    if not data or 'content' not in data:
        abort(400, description="Campo 'content' é obrigatório.")
    
    new_message = Message(content=data['content'])
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify(new_message.to_dict()), 201

@messages_bp.route('/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    message = Message.query.get_or_404(message_id)
    data = request.get_json()
    if not data or 'content' not in data:
        abort(400, description="Campo 'content' é obrigatório.")
    
    message.content = data['content']
    db.session.commit()
    
    return jsonify(message.to_dict()), 200

@messages_bp.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    
    return '', 204
