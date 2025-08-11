from marshmallow import Schema, fields, validate

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    conteudo = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    data_criacao = fields.DateTime(dump_only=True)
    autor_id = fields.Int(dump_only=True)
    mensagem_id = fields.Int(required=True)