from marshmallow import Schema, fields, validate

class MessageSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    conteudo = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    data_criacao = fields.DateTime(dump_only=True)
    curtidas = fields.Int(dump_only=True)  # curtidas só leitura
    user_id = fields.Int(required=True)
    deleted = fields.Bool(dump_only=True)
