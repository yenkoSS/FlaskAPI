from marshmallow import Schema, fields


class StorePostSchema(Schema):

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)


class StoreUpdateSchema(Schema):

    name = fields.String(required=True)




