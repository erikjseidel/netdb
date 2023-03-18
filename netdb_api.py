from flask          import Flask, Response, request, json
from util.netdb     import NetDB
from util.netdb_orm import NetdbORM
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

    netdb = NetDB(column = column)

    if request.method == 'POST':
        to_mongo = NetdbORM(data, column).saltToMongo()

        if to_mongo['result']:
            response = netdb.save(to_mongo['out'])
        else:
            response = to_mongo

    elif request.method == 'GET':
        mongo_out = netdb.fetch(id_key = device_id)

        if mongo_out['result']:
            response = NetdbORM(mongo_out['out'], column).mongoToSalt()
        else:
            response = mongo_out
    else:
        response = netdb.delete({ 'id': device_id })

    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
