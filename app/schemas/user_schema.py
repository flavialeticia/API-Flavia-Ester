from .. import ma
from marshmallow import Schema, fields, post_load
from ..models.user import User

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    nome = fields.Str(required=True)
    senha = fields.Str(load_only=True, required=True)  # senha só para load (não envia na resposta)
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
