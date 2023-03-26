
from marshmallow import Schema, fields, validate, INCLUDE, ValidationError

from .netdb_column      import netdbColumn

class igpIsisInterfaceSchema(Schema):
    name    = fields.String(required = True)
    passive = fields.Bool()


class igpIsisSchema(Schema):
    level       = fields.Integer(required = True, validate = validate.OneOf([1,2]))
    lsp_mtu     = fields.Integer(required = True, validate = validate.Range(min=1200, max=9200))
    iso         = fields.String(required = True)

    interfaces  = fields.List(fields.Nested(igpIsisInterfaceSchema()))

    redistribute = fields.Dict(required=True, keys = fields.String(required=True, validate=validate.OneOf(['ipv4','ipv6'])),
            values = fields.Dict(required=True, keys = fields.String(required=True, validate=validate.OneOf(['level_1','level_2'])),
                values = fields.Dict(requires=True, keys = fields.String(required=True), values = fields.String() )))


class netdbIgp(netdbColumn):

    _COLUMN     = 'igp'

    _COLUMN_CAT  = {
            'type_1'   :  [],
            'type_2'   :  [],
            'type_3'   :  [ 'isis' ],
            }

    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        for top_id, config_data in self.data.items():
            if top_id.startswith('_'):
                if 'roles' not in config_data:
                    return { 'result': False, 'comment': "%s: roles required for shared config set" % top_id }

            try:
                igpIsisSchema().load(config_data['isis'])
            except ValidationError as error:
                return { 'result': False, 'comment': '%s: invalid data' % top_id, 'out': error.messages }

        return { 'result': True, 'comment': '%s - all checks passed' % top_id }

