from marshmallow import Schema, fields, validate, INCLUDE, ValidationError
from util import netdb_fields

class firewallMssSchema(Schema):
    ipv4 = fields.Integer(required=True, validate=validate.Range(min=556, max=9172))
    ipv6 = fields.Integer(validate=validate.Range(min=1280, max=9172))

    interfaces = fields.List(fields.String())


class firewallStateSchema(Schema):
    established = fields.String(validate=validate.OneOf(['accept', 'drop']))
    related     = fields.String(validate=validate.OneOf(['accept', 'drop']))


class firewallOptionsSchema(Schema):
    class Meta:
        include = {
            'all-ping':                 fields.String(),
            'broadcast-ping':           fields.String(),
            'config-trap':              fields.String(),
            'ipv6-receive-redirects':   fields.String(),
            'ipv6-src-route':           fields.String(),
            'log-martians':             fields.String(),
            'send-redirects':           fields.String(),
            'source-validation':        fields.String(),
            'syn-cookies':              fields.String(),
            'twa-hazards-protection':   fields.String(),
            'ip-src-route':             fields.String(),
            'receive-redirect':         fields.String(),
            }

class firewallZoneRulesSchema(Schema):
    ipv4_ruleset = fields.String()
    ipv6_ruleset = fields.String()

    zone = fields.String(required=True)

class firewallZoneSchema(Schema):
    class Meta:
        include = {
                'from': fields.List(fields.Nested(firewallZoneRulesSchema()), validate=validate.Length(min=1))
                }

    interfaces = fields.List(fields.String())

    default_action = fields.String(validate=validate.OneOf(['accept','drop']))


class firewallGroup4NamesSchema(Schema):
    class Meta:
        include = {
                'type': fields.String(required=True, validate=validate.OneOf(['network']))
                }
    
    networks = fields.List(netdb_fields.netdbIPv4Interface(), validate=validate.Length(min=1))


class firewallGroup6NamesSchema(Schema):
    class Meta:
        include = {
                'type': fields.String(required=True, validate=validate.OneOf(['network']))
                }
    
    networks = fields.List(netdb_fields.netdbIPv6Interface(), validate=validate.Length(min=1))


class firewallGroupSchema(Schema):
    ipv4 = fields.Dict(keys=fields.String(required=True), values=fields.Nested(firewallGroup4NamesSchema()))
    ipv6 = fields.Dict(keys=fields.String(required=True), values=fields.Nested(firewallGroup6NamesSchema()))


class firewallPolicyTargetSchema(Schema):
    network_group = fields.String()
    port = fields.List(fields.Integer(), validate=validate.Length(min=1))


class firewallPolicyRulesSchema(Schema):
    action = fields.String(required=True, validate=validate.OneOf(['accept','drop']))
    source = fields.Nested(firewallPolicyTargetSchema())
    destination = fields.Nested(firewallPolicyTargetSchema())

    state    = fields.List(fields.String(validate=validate.OneOf(['established', 'related'])), validate=validate.Length(min=1,max=2))
    protocol = fields.String()


class firewallPolicyNamesSchema(Schema):
    default_action = fields.String(required=True, validate=validate.OneOf(['accept','drop']))
    
    rules = fields.List(fields.Nested(firewallPolicyRulesSchema()))


class firewallPolicySchema(Schema):
    ipv4 = fields.Dict(keys=fields.String(required=True), values=fields.Nested(firewallPolicyNamesSchema()))
    ipv6 = fields.Dict(keys=fields.String(required=True), values=fields.Nested(firewallPolicyNamesSchema()))


class firewallSchema(Schema):
    policies     = fields.Nested(firewallPolicySchema())
    groups       = fields.Nested(firewallGroupSchema())
    options      = fields.Nested(firewallOptionsSchema())
    state_policy = fields.Nested(firewallStateSchema())
    mss_clamp    = fields.Nested(firewallMssSchema())

    zone_policy  = fields.Dict( keys=fields.String(required=True), values=fields.Nested(firewallZoneSchema()) )
