from marshmallow import Schema, fields, validate


class EditSubscriptionSchema(Schema):
    id = fields.Integer(dump_only=True)
    lat = fields.Float(required=True)
    lon = fields.Float(required=True)
    hours = fields.List(fields.Integer, required=True, validate=validate.Length(min=1))  # TODO: dump do poprawy


class NewSubscriptionSchema(EditSubscriptionSchema):
    email = fields.Email(required=True)


edit_sub_schema = EditSubscriptionSchema()
new_sub_schema = NewSubscriptionSchema()
