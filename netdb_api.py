from flask import Flask, Response, request, json

import models, builders
import models.netdb     as netdb
import builders.builder as builder

app = Flask(__name__)

def handle_bad_request(e):
    return json.dumps({ 'result': False, 'comment': 'bad request' }), 400

app.register_error_handler(400, handle_bad_request)

@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')
  

@app.route('/api/<column>',                methods=['GET', 'POST', 'DELETE'])
@app.route('/api/<column>/<top_id>',       methods=['GET', 'POST', 'DELETE'])
@app.route('/api/<column>/<top_id>/<opt>', methods=['GET'])
def api_entry(column, top_id = None, opt = None):

    if column not in netdb.COLUMNS or opt not in [ None, 'config']:
        return Response(response=json.dumps({"result": False, "comment": "Invalid endpoint"}),
                        status=400,
                        mimetype='application/json')

    if request.method in ['POST']:
        data = request.json
        if data is None or data == {}:
            return Response(response=json.dumps({"Error": "No input data"}),
                            status=400,
                            mimetype='application/json')

    if request.method == 'GET':
        if not top_id:
            query = {}
        elif column in ['device']:
            query = { "id": top_id }
        else:
            query = { "set_id": top_id }

        if opt == 'config':
            response = builder.newBuilder(column, top_id).build()
        else:
            response = netdb.newColumn(column).fetch(query)

    elif request.method == 'POST':
        response = netdb.newColumn(column).set(data).save()

    else:
        response = db.delete({ 'id': top_id })

    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
