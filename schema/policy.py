from marshmallow import Schema, fields, validate, INCLUDE, ValidationError
from util import netdb_fields

class policyCommAspathListRulesSchema(Schema):
    description = fields.String()
    action = fields.String(validate=validate.OneOf(['permit', 'deny']))
    regex = fields.String(required=True)


class policyAspathListSchema(Schema):
    description = fields.String()
    rules = fields.List(fields.Nested(policyCommAspathListRulesSchema()), required=True, validate=validate.Length(min=1))


class policyCommunityListSchema(Schema):
    description = fields.String()
    rules = fields.List(fields.Nested(policyCommAspathListRulesSchema()), required=True, validate=validate.Length(min=1))


class policyList4RulesSchema(Schema):
    le = fields.Integer(validate=validate.Range(min=0, max=32))
    ge = fields.Integer(validate=validate.Range(min=0, max=32))

    prefix = netdb_fields.netdbIPv4Interface(required=True)


class policyList4NamesSchema(Schema):
    rules = fields.List(fields.Nested(policyList4RulesSchema()), required=True, validate=validate.Length(min=1))


class policyList6RulesSchema(Schema):
    le = fields.Integer(validate=validate.Range(min=0, max=128))
    ge = fields.Integer(validate=validate.Range(min=0, max=128))

    prefix = netdb_fields.netdbIPv6Interface(required=True)


class policyList6NamesSchema(Schema):
    rules = fields.List(fields.Nested(policyList6RulesSchema()), required=True, validate=validate.Length(min=1))


class policyPrefixListSchema(Schema):
    ipv4 = fields.Dict(keys=fields.String(required=True), values=fields.Nested(policyList4NamesSchema()))
    ipv6 = fields.Dict(keys=fields.String(required=True), values=fields.Nested(policyList6NamesSchema()))


class policyMapMatchSchema(Schema):
    prefix_list    = fields.String()
    community_list = fields.String()
    as_path        = fields.String()

    rpki = fields.String(validate=validate.OneOf(['notfound', 'valid', 'invalid']))


class policyMapSetSchema(Schema):
    local_pref = fields.Integer(validate=validate.Range(min=0, max=255))
    next_hop   = netdb_fields.netdbIP()
    origin     = fields.String()

    community        = fields.String()
    large_community  = fields.String()
    as_path_exclude  = fields.Integer(validate=validate.Range(min=1,max=2**32))


class policyMapRulesSchema(Schema):
    class Meta:
        include = {
                'set':      fields.Nested(policyMapSetSchema()),
                'continue': fields.Integer(validate=validate.Range(min=0, max=999)),
                }

    match  = fields.Nested(policyMapMatchSchema())
    number = fields.Integer(required=True, validate=validate.Range(min=0, max=999))
    action = fields.String(required=True, validate=validate.OneOf(['permit', 'deny']))


class policyMapNamesSchema(Schema):
    rules = fields.List(fields.Nested(policyMapRulesSchema()), required=True, validate=validate.Length(min=1))


class policyRouteMapSchema(Schema):
    ipv4 = fields.Dict(keys=fields.String(required=True), values=fields.Nested(policyMapNamesSchema()))
    ipv6 = fields.Dict(keys=fields.String(required=True), values=fields.Nested(policyMapNamesSchema()))


class policySchema(Schema):
    prefix_lists = fields.Nested(policyPrefixListSchema())
    route_maps   = fields.Nested(policyRouteMapSchema())

    aspath_lists    = fields.Dict(keys=fields.String(required=True), values=fields.Nested(policyAspathListSchema()))
    community_lists = fields.Dict(keys=fields.String(required=True), values=fields.Nested(policyCommunityListSchema()))
