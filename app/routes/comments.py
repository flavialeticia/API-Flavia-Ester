from flask import Blueprint, request, jsonify, g
from ..models.comment import Comment
from ..models.message import Message
from ..models.user import User
from .. import db
from ..schemas.comment_schema import CommentSchema
from ..decorators.jwt_decorators import jwt_required, require_role

comments_bp = Blueprint('comments', __name__)
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

@comments_bp.route('/', methods=['POST'])
@jwt_required
def create_comment():
    data = request.get_json()
    conteudo = data.get('conteudo')
    mensagem_id = data.get('mensagem_id')

    if not conteudo:
        return jsonify({'error': 'Conteúdo do comentário não pode ser vazio'}), 400

    mensagem = Message.query.get(mensagem_id)
    if not mensagem:
        return jsonify({'error': 'Mensagem não encontrada'}), 404

    comment = Comment(
        conteudo=conteudo,
        autor_id=g.current_user.id,
        mensagem_id=mensagem_id
    )

    db.session.add(comment)
    db.session.commit()
    return jsonify(comment_schema.dump(comment)), 201

@comments_bp.route('/<int:comment_id>', methods=['PUT'])
@jwt_required
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.autor_id != g.current_user.id and g.current_user.perfil != 'ADMIN':
        return jsonify({'error': 'Somente o autor ou administrador pode editar'}), 403

    data = request.get_json()

    if 'autor_id' in data or 'mensagem_id' in data:
        return jsonify({'error': 'Não é permitido modificar autor_id ou mensagem_id'}), 400

    if 'conteudo' in data:
        if not data['conteudo']:
            return jsonify({'error': 'Conteúdo do comentário não pode ser vazio'}), 400
        comment.conteudo = data['conteudo']

    db.session.commit()
    return jsonify(comment_schema.dump(comment)), 200

@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.autor_id != g.current_user.id and g.current_user.perfil != 'ADMIN':
        return jsonify({'error': 'Acesso negado'}), 403
    db.session.delete(comment)
    db.session.commit()
    return '', 204

@comments_bp.route('/message/<int:mensagem_id>', methods=['GET'])
def get_comments_by_message(mensagem_id):
    mensagem = Message.query.get_or_404(mensagem_id)
    comments = Comment.query.filter_by(mensagem_id=mensagem.id).all()
    return jsonify(comments_schema.dump(comments)), 200
