from .. import ma
from marshmallow import fields, validate
from ..models.message import Message

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True  
        fields = ("id", "content", "created_at")  # mantém a ordem do modelo
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True, validate=validate.Length(min=1, max=140))
    created_at = fields.DateTime(dump_only=True)