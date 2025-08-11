from marshmallow import Schema, fields, validate, ValidationError

class MessageSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    conteudo = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    data_criacao = fields.DateTime(dump_only=True)
    user_id = fields.Int(required=True)