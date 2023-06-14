from marshmallow import Schema, fields, validate, INCLUDE, ValidationError

class igpIsisInterfaceSchema(Schema):
    name    = fields.String(required = True)
    passive = fields.Bool()


class igpIsisSchema(Schema):
    level       = fields.Integer(validate = validate.OneOf([1,2]))
    lsp_mtu     = fields.Integer(validate = validate.Range(min=1200, max=9200))
    iso         = fields.String()

    interfaces  = fields.List(fields.Nested(igpIsisInterfaceSchema()))

    redistribute = fields.Dict(keys = fields.String(required=True, validate=validate.OneOf(['ipv4','ipv6'])),
            values = fields.Dict(required=True, keys = fields.String(required=True, validate=validate.OneOf(['level_1','level_2'])),
                values = fields.Dict(requires=True, keys = fields.String(required=True), values = fields.String() )))

    # netdb metadata and control
    meta       = fields.Dict()
    weight     = fields.Integer(validate=validate.Range(min=50, max=1001))
    datasource = fields.String()

class igpSchema(Schema):
    isis = fields.Nested(igpIsisSchema())

    roles = fields.List(fields.String(), validate=validate.Length(min=1))
