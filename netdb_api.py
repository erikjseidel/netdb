from flask import Flask, Response, request, json

import models, builders
import models.netdb     as netdb
import builders.builder as builder

app = Flask(__name__)


ERR_INVALID_EP = Response(response = json.dumps({ "result": False, "comment": "Invalid endpoint"} ),
                        status = 200, mimetype = 'application/json')

ERR_INVALID_DATA = Response(response = json.dumps({ "result": False, "comment": "Invalid input data" }),
                        status = 400, mimetype = 'application/json')


def handle_bad_request(e):
    return json.dumps({ 'result': False, 'comment': 'bad request' }), 400

app.register_error_handler(400, handle_bad_request)


def get_data(request):
    if not request.data:
        return None

    data = request.json
    if not ( isinstance(data, list) or isinstance(data, dict) ):
        return None

    return data


@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')
  

@app.route('/api/<column>/<top_id>/config', methods=['GET'])
def builder_route(column, top_id):
    if column not in netdb.COLUMNS:
        return ERR_INVALID_EP

    # device and interface columns do not need config builders.
    if column not in ['device', 'interface']:
        response = builder.newBuilder(column, top_id).build()
    else:
        response = netdb.newColumn(column).filter(top_id).fetch()

    return Response(response=json.dumps(response), status=status, mimetype='application/json')


@app.route('/api/<column>/validate', methods=['POST', 'PUT'])
def validator_route(column):
    if column not in netdb.COLUMNS:
        return ERR_INVALID_EP

    if not ( data := get_data(request) ):
        return ERR_INVALID_DATA

    response = netdb.newColumn(column).set(data).validate()

    return Response(response=json.dumps(response), status=200, mimetype='application/json')


@app.route('/api/<column>/project', methods=['GET'])
def projector_route(column):
    if column not in netdb.COLUMNS:
        return ERR_INVALID_EP

    if not ( data := get_data(request) ):
        return ERR_INVALID_DATA

    response = netdb.newColumn(column).project(data).fetch()

    return Response(response=json.dumps(response), status=200, mimetype='application/json')


@app.route('/api/<column>', methods=['POST', 'PUT', 'DELETE'])
def alter_route(column):
    if column not in netdb.COLUMNS:
        return ERR_INVALID_EP

    if not ( data := get_data(request) ):
        return ERR_INVALID_DATA

    if request.method == 'POST':
        response = netdb.newColumn(column).set(data).save()

    elif request.method == 'PUT':
        response = netdb.newColumn(column).set(data).update()

    elif request.method == 'DELETE':
        response = netdb.newColumn(column).filter(data).delete()

    return Response(response=json.dumps(response), status=200, mimetype='application/json')


@app.route('/api/<column>',          methods=['GET'])
@app.route('/api/<column>/<top_id>', methods=['GET'])
def fetcher_route(column, top_id = None):
    if column not in netdb.COLUMNS:
        return ERR_INVALID_EP

    data = get_data(request)

    if data:
        response = netdb.newColumn(column).filter(data).fetch()
    else:
        response = netdb.newColumn(column).filter(top_id).fetch()

    return Response(response=json.dumps(response), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
