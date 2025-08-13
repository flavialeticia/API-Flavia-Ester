from datetime import datetime
from .. import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    curtidas = db.Column(db.Integer, default=0)  # novo campo curtidas
    deleted = db.Column(db.Boolean, default=False)  # para soft delete
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_message_user'), nullable=False, default=1)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'conteudo': self.conteudo,
            'data_criacao': self.data_criacao.isoformat(),
            'curtidas': self.curtidas,
            'user_id': self.user_id
        }
