from flask          import Flask, Response, request, json

from models.netdb_device    import netdbDevice
from models.netdb_interface import netdbInterface

import yaml
app = Flask(__name__)

def handle_bad_request(e):
    return json.dumps({ 'result': False, 'comment': 'bad request' }), 400

app.register_error_handler(400, handle_bad_request)

@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')
  

@app.route('/api/<column>', methods=['GET', 'POST', 'DELETE'])
@app.route('/api/<column>/<device_id>', methods=['GET', 'POST', 'DELETE'])
def api_entry(column, device_id = None):

    if column not in ['device', 'interface']:
        return Response(response=json.dumps({"result": False, "comment": "Invalid endpoint"}),
                        status=400,
                        mimetype='application/json')

    if request.method in ['POST']:
        data = request.json
        if data is None or data == {}:
            return Response(response=json.dumps({"Error": "No input data"}),
                            status=400,
                            mimetype='application/json')

    if column == 'device':
        netdb = netdbDevice()  
    if column == 'interface':
        netdb = netdbInterface()  

    if request.method == 'POST':
        netdb.set(data)
        response = netdb.save()

    elif request.method == 'GET':
        if not device_id:
            query = {}
        else:
            query = { "id": device_id }

        response = netdb.fetch(query)

    else:
        response = netdb.delete({ 'id': device_id })

    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
