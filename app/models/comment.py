from datetime import datetime
from .. import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_comment_user'), nullable=False)
    mensagem_id = db.Column(db.Integer, db.ForeignKey('message.id', name='fk_comment_message'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'conteudo': self.conteudo,
            'data_criacao': self.data_criacao.isoformat(),
            'autor_id': self.autor_id,
            'mensagem_id': self.mensagem_id
        }