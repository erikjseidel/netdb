from flask          import Flask, Response, request, json

from models.netdb_device    import netdbDevice
from models.netdb_interface import netdbInterface
from models.netdb_igp       import netdbIgp
from models.netdb_firewall  import netdbFirewall
from models.netdb_policy    import netdbPolicy

from builders.igp_config_builder       import igpConfigBuilder
from builders.firewall_config_builder  import firewallConfigBuilder
from builders.policy_config_builder    import policyConfigBuilder
from builders.interface_config_builder import interfaceConfigBuilder

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
@app.route('/api/<column>/<top_id>', methods=['GET', 'POST', 'DELETE'])
@app.route('/api/<column>/<top_id>/<opt>', methods=['GET'])
def api_entry(column, top_id = None, opt = None):

    if column not in ['device', 'interface', 'igp', 'firewall', 'policy'] or opt not in [ None, 'config']:
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
    if column == 'igp':
        netdb = netdbIgp()  
    if column == 'firewall':
        netdb = netdbFirewall()  
    if column == 'policy':
        netdb = netdbPolicy()  

    if request.method == 'POST':
        netdb.set(data)
        response = netdb.save()

    elif request.method == 'GET':
        if not top_id:
            query = {}
        elif column in ['igp', 'firewall', 'policy']:
            query = { "set_id": top_id }
        else:
            query = { "id": top_id }

        if column in ['igp'] and opt == 'config':
            response = igpConfigBuilder(top_id).build()
        elif column in ['firewall'] and opt == 'config':
            response = firewallConfigBuilder(top_id).build()
        elif column in ['policy'] and opt == 'config':
            response = policyConfigBuilder(top_id).build()
        elif column in ['interface'] and opt == 'config':
            response = interfaceConfigBuilder(top_id).build()
        else:
            response = netdb.fetch(query)

    else:
        response = netdb.delete({ 'id': top_id })

    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
