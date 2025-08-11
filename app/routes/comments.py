from flask import Blueprint, request, jsonify, g
from ..models.comment import Comment
from ..models.message import Message
from .. import db
from ..schemas.comment_schema import CommentSchema
from ..decorators.jwt_decorators import jwt_required

# Blueprint with prefix for all routes
comments_bp = Blueprint('comments', __name__, url_prefix='/messages')

# Schemas initialization
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

@comments_bp.route('/<int:message_id>/comentarios', methods=['POST'])
@jwt_required
def create_comment(message_id):
    """Create a new comment on a message"""
    data = request.get_json()
    
    # Validation
    if not data or not data.get('conteudo'):
        return jsonify({'error': 'Comment content is required'}), 400

    # Check if message exists
    if not Message.query.get(message_id):
        return jsonify({'error': 'Message not found'}), 404

    # Create comment
    comment = Comment(
        conteudo=data['conteudo'],
        autor_id=g.current_user.id,
        mensagem_id=message_id
    )

    db.session.add(comment)
    db.session.commit()
    return jsonify(comment_schema.dump(comment)), 201

@comments_bp.route('/<int:message_id>/comentarios', methods=['GET'])
def get_comments(message_id):
    """Get all comments for a message"""
    # Check if message exists
    if not Message.query.get(message_id):
        return jsonify({'error': 'Message not found'}), 404
        
    comments = Comment.query.filter_by(mensagem_id=message_id).all()
    return jsonify(comments_schema.dump(comments)), 200

@comments_bp.route('/<int:message_id>/comentarios/<int:comment_id>', methods=['PUT'])
@jwt_required
def update_comment(message_id, comment_id):
    """Update a comment"""
    comment = Comment.query.filter_by(
        id=comment_id,
        mensagem_id=message_id
    ).first_or_404()

    # Authorization
    if comment.autor_id != g.current_user.id and g.current_user.perfil != 'ADMIN':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    
    # Validation
    if not data or not data.get('conteudo'):
        return jsonify({'error': 'Comment content is required'}), 400
        
    comment.conteudo = data['conteudo']
    db.session.commit()
    
    return jsonify(comment_schema.dump(comment)), 200

@comments_bp.route('/<int:message_id>/comentarios/<int:comment_id>', methods=['DELETE'])
@jwt_required
def delete_comment(message_id, comment_id):
    """Delete a comment"""
    comment = Comment.query.filter_by(
        id=comment_id,
        mensagem_id=message_id
    ).first_or_404()

    # Authorization
    if comment.autor_id != g.current_user.id and g.current_user.perfil != 'ADMIN':
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(comment)
    db.session.commit()
    return '', 204