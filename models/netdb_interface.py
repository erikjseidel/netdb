
from marshmallow import Schema, fields, validate, INCLUDE, ValidationError

from .netdb_column      import netdbColumn

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

    address     = fields.Dict(keys = fields.IPInterface(), values = fields.Nested(addressMetaSchema))
    description = fields.String()
    interface   = fields.String()

    mtu = fields.Integer(validate=validate.Range(min=1280,max=9192))
    ttl = fields.Integer(validate=validate.Range(min=1,max=255))

    remote = fields.IP()
    source = fields.IP()

    firewall = fields.Dict(keys = fields.String(required=True, validate=validate.OneOf(['local','ingress','egress'])),
                values = fields.Dict(keys = fields.String(required=True, validate=validate.OneOf(['ipv4','ipv6'])),
                    values = fields.String(required=True) ))

    policy = fields.Dict(keys = fields.String(required=True, validate=validate.OneOf(['ipv4','ipv6'])),
                            values = fields.String(required=True))

    lacp = fields.Nested(lacpOptionsSchema)
    vlan = fields.Nested(vlanOptionsSchema)


class netdbInterface(netdbColumn):

    _COLUMN     = 'interface'

    _COLUMN_CAT  = {
            'type_1'   :  [],
            'type_2'   :  [ 'interfaces' ],
            'type_3'   :  [],
            }


    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        for top_id, interfaces in self.data.items():
            if 'interfaces' not in interfaces:
                return { 'result': False, 'comment': "%s: interfaces set not found" % top_id }

            if top_id.startswith('_'):
                if 'roles' not in config_data:
                    return { 'result': False, 'comment': "%s: roles required for shared config set" % top_id }

            for iface, iface_data in interfaces['interfaces'].items():
                try:
                    interfaceSchema().load(iface_data)
                except ValidationError as error:
                    return { 'result': False, 'comment': '%s: invalid data' % top_id, 'out': error.messages }

        return { 'result': True, 'comment': '%s: all checks passed' % top_id }
