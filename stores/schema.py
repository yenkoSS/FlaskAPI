from marshmallow import Schema, fields


class CreateStoreSchema(Schema):

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)


class UpdateStoreSchema(Schema):

    name = fields.String(required=True)




