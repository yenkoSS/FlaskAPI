from marshmallow import Schema, fields


class ItemPostSchema(Schema):

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)


class ItemUpdateSchema(Schema):

    name = fields.String()
    price = fields.Float()
