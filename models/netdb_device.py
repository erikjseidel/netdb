
from marshmallow import Schema, fields, validate, INCLUDE, ValidationError

from .netdb_column      import netdbColumn

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


class netdbDevice(netdbColumn):

    _COLUMN     = 'device'

    def filter(self, filt):
        if not filt:
            pass

        elif isinstance(filt, dict):
            self._FILT = filt

        else:
            self._FILT = { 'id': filt }

        return self


    def _to_mongo(self, data):
        out = []

        for device, elements in data.items():
            entry = { 'id' : device }
            entry.update(elements)

            out.append(entry)

        return out


    def _from_mongo(self, data):
        out = {}

        for device in data:
            device_id  = device.pop('id')
            out[device_id] = device

        return out


    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        for top_id, device in self.data.items():
            try:
                deviceSchema().load(device)
            except ValidationError as error:
                return { 'result': False, 'comment': '%s: invalid data' % top_id, 'out': error.messages }

        return { 'result': True, 'comment': '%s - all checks passed' }
