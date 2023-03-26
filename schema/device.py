
from marshmallow import Schema, fields, validate, INCLUDE, ValidationError

class cvarsSchema(Schema):
    class Meta:
        unknown = INCLUDE

    # defined cvars
    ibgp_ipv4 = fields.IPv4()
    ibgp_ipv6 = fields.IPv6()
    iso       = fields.String()
    router_id = fields.IPv4(required=True)
    local_asn = fields.Integer(required=True, validate=validate.Range(min=1, max=2**32))


class deviceSchema(Schema):
    location  = fields.String(required = True)
    providers = fields.List(fields.String(), required = True, validate=validate.Length(min=1))
    roles     = fields.List(fields.String(), required = True, validate=validate.Length(min=1))
    cvars     = fields.Nested(cvarsSchema)

    downstream_asns = fields.List(fields.Integer(), validate=validate.Length(min=1))
    ibgp_ipv4       = fields.IPv4()
    ibgp_ipv6       = fields.IPv6()
    iso             = fields.String()
    local_asn       = fields.Integer()
