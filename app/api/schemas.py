from marshmallow import Schema, fields, validate


class EditSubscriptionSchema(Schema):
    id = fields.Integer(dump_only=True)
    lat = fields.Float(required=True)
    lon = fields.Float(required=True)
    hours = fields.Method("get_hours", deserialize="load_hours", required=True, validate=validate.Length(min=1))

    def get_hours(self, obj):  # TODO:  unit testy
        return obj.get_int_hours()

    def load_hours(self, value):  # TODO: unit testy
        return value


class NewSubscriptionSchema(EditSubscriptionSchema):
    email = fields.Email(required=True)


edit_sub_schema = EditSubscriptionSchema()
new_sub_schema = NewSubscriptionSchema()
