
from marshmallow import Schema, fields, validate, INCLUDE, ValidationError
from util        import netdb_fields

class bgpOptionsSchema(Schema):
    asn       = fields.String(required=True)
    router_id = netdb_fields.netdbIPv4(required=True)

    hold_time      = fields.Integer(validate=validate.Range(min=15,max=180))
    keepalive_time = fields.Integer(validate=validate.Range(min=5,max=60))

    log_neighbor_changes = fields.Bool()


class bgpPeerFamilyMapSchema(Schema):
    class Meta:
        include = {
                'import': fields.String(required=True),
                }

    export = fields.String(required=True)


class bgpPeerFamilyOptSchema(Schema):
    nhs = fields.Bool()
    route_map = fields.Nested(bgpPeerFamilyMapSchema())


class bgpPeerFamilySchema(Schema):
    ipv4 = fields.Nested(bgpPeerFamilyOptSchema())
    ipv6 = fields.Nested(bgpPeerFamilyOptSchema())


class bgpNeighborSchema(Schema):
    class Meta:
        include = {
                'type':      fields.String(validate=validate.OneOf(['ibgp', 'ebgp'])),
                }
    source = fields.String()
    family = fields.Nested(bgpPeerFamilySchema())
 
    multihop = fields.Integer(validate=validate.Range(min=1,max=255))
    password = fields.String()

    peer_group = fields.String(required=True)
    remote_asn = fields.Integer()

    timers = fields.Dict(
            keys=fields.String(validate=validate.OneOf(['keepalive','holdtime'])), 
            values=fields.Integer(validate=validate.Range(min=10,max=1000))
            )

    # netdb metadata and control
    meta       = fields.Dict()
    weight     = fields.Integer(validate=validate.Range(min=50, max=1001))
    datasource = fields.String()


class bgpPeerGroupSchema(Schema):
    class Meta:
        include = {
                'type':      fields.String(validate=validate.OneOf(['ibgp', 'ebgp'])),
                }
    source = netdb_fields.netdbIP()
    family = fields.Nested(bgpPeerFamilySchema())

    multihop = fields.Integer(validate=validate.Range(min=1,max=255))
    password = fields.String()

    remote_asn = fields.Integer()

    timers = fields.Dict(
            keys=fields.String(validate=validate.OneOf(['keepalive','holdtime'])), 
            values=fields.Integer(validate=validate.Range(min=10,max=1000))
            )

    # netdb metadata and control
    meta       = fields.Dict()
    weight     = fields.Integer(validate=validate.Range(min=50, max=1001))
    datasource = fields.String()


class bgpAddressFamilyContentsSchema(Schema):
    networks     = fields.Dict(keys = fields.String())
    redistribute = fields.Dict(keys = fields.String())


class bgpAddressFamilySchema(Schema):
    ipv4 = fields.Nested(bgpAddressFamilyContentsSchema())
    ipv6 = fields.Nested(bgpAddressFamilyContentsSchema())


class bgpSchema(Schema):
    address_family = fields.Nested(bgpAddressFamilySchema())
    options        = fields.Nested(bgpOptionsSchema())

    peer_groups = fields.Dict(keys=fields.String(required=True), values=fields.Nested(bgpPeerGroupSchema()))
    neighbors   = fields.Dict(keys=fields.String(required=True), values=fields.Nested(bgpNeighborSchema()))

    roles = fields.List(fields.String(), validate=validate.Length(min=1))

