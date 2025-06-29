from marshmallow import Schema, fields

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    conteudo = fields.Str(required=True)
    dataHora = fields.DateTime(dump_only=True)
    autor_id = fields.Int(dump_only=True)
    mensagem_id = fields.Int(required=True)