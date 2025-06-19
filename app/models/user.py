from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
import re

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='author', lazy=True)

    @property
    def senha(self):
        raise AttributeError('senha não é um atributo legível')

    @senha.setter
    def senha(self, senha):
        if not self.validar_senha(senha):
            raise ValueError('Senha não atende aos requisitos de segurança')
        self.senha_hash = generate_password_hash(senha)

    def validar_senha(self, senha):
        if len(senha) < 8:
            return False
        if not re.search(r"[A-Z]", senha):
            return False
        if not re.search(r"[a-z]", senha):
            return False
        if not re.search(r"[0-9]", senha):
            return False
        if not re.search(r"[@!%*?&]", senha):
            return False
        return True

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nome': self.nome,
            'created_at': self.created_at.isoformat()
        }