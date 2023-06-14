from marshmallow import Schema, fields, validate, INCLUDE, ValidationError
from util import netdb_fields

IFACE_TYPES = ['ethernet', 'vlan', 'lacp', 'dummy', 'gre', 'l2gre']

class addressMetaSchema(Schema):
    meta = fields.Dict(keys = fields.String(required=True))


class lacpOptionsSchema(Schema):
    hash_policy = fields.String(required=True, validate=validate.OneOf(['layer2+3','layer3+4']))
    rate        = fields.String(required=True, validate=validate.OneOf(['fast','slow']))
    members     = fields.List(fields.String())
    min_links   = fields.Integer(required=True, validate=validate.Range(min=1, max=5))


class vlanOptionsSchema(Schema):
    class Meta:
        include = {
                'id': fields.Integer(required=True, validate=validate.Range(min=1, max=4096))
                }

    parent = fields.String(required=True)


class interfaceSchema(Schema):
    class Meta:
        include = {
                'type': fields.String(required=True, validate=validate.OneOf(IFACE_TYPES))
                }

    disabled    = fields.Bool()

    address     = fields.Dict(keys = netdb_fields.netdbIPInterface(), values = fields.Nested(addressMetaSchema))
    description = fields.String()
    interface   = fields.String()
    mac_address = fields.String()

    mtu = fields.Integer(validate=validate.Range(min=1280,max=9192))
    ttl = fields.Integer(validate=validate.Range(min=1,max=255))
    key = netdb_fields.netdbIPv4()

    offload = fields.Bool()

    remote = netdb_fields.netdbIP()
    source = netdb_fields.netdbIP()

    firewall = fields.Dict(keys = fields.String(required=True, validate=validate.OneOf(['local','ingress','egress'])),
                values = fields.Dict(keys = fields.String(required=True, validate=validate.OneOf(['ipv4','ipv6'])),
                    values = fields.String(required=True) ))

    policy = fields.Dict(keys = fields.String(required=True, validate=validate.OneOf(['ipv4','ipv6'])),
                            values = fields.String(required=True))

    lacp = fields.Nested(lacpOptionsSchema)
    vlan = fields.Nested(vlanOptionsSchema)

    # netdb metadata and control
    meta       = fields.Dict()
    weight     = fields.Integer(validate=validate.Range(min=50, max=1001))
    datasource = fields.String()
