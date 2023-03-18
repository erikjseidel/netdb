

# Maps column types to column keys
ELEMENT_ID = {
        'device'   : 'id',
        'interface': 'interface_id',
        }
 
class NetdbORM:

    def __init__(self, data, column):
        self.data   = data
        self.column = column


    def saltToMongo(self):
        out = []

        for device, elements in self.data.items():
            if self.column == 'device':
                entry = { 'id' : device }
                entry.update(elements)

                out.append(entry)
            else:
                for element, contents in elements.items():
                    entry = { 'id' : device, ELEMENT_ID[self.column] : element }
                    entry.update(contents)

                    out.append(entry)

        return { 'result': True, 'out': out }


    def mongoToSalt(self):
        out = {}

        if self.column == 'device':
            for device in self.data:
                device_id  = device.pop('id')
                out[device_id] = device

        else:
            for entry in self.data:
                element_key = ELEMENT_ID[self.column]
                element_id  = entry.pop(element_key)
                device_id   = entry.pop('id')

                if device_id not in out:
                    out[device_id] = {}

                out[device_id][element_id] = entry

        return { 'result': True, 'out': out }
