from marshmallow import Schema, fields


class SubscriptionSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    lat = fields.Float(required=True)
    lon = fields.Float(required=True)
    hours = fields.List(fields.Integer, required=True)


subscription_schema = SubscriptionSchema()
