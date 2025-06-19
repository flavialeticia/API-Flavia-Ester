from marshmallow import Schema, fields, validate, validates, ValidationError
import re

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True, validate=validate.Email())
    nome = fields.Str(required=True, validate=validate.Length(min=1))
    senha = fields.Str(required=True, load_only=True, validate=validate.Length(min=8))
    created_at = fields.DateTime(dump_only=True)

    @validates('email')
    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValidationError("Formato de email inválido")