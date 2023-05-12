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
  

@app.route('/api/<column>',                methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/<column>/<top_id>',       methods=['GET', 'POST', 'PUT'])
@app.route('/api/<column>/<top_id>/<opt>', methods=['GET'])
def api_entry(column, top_id = None, opt = None):

    if column not in netdb.COLUMNS or opt not in [ None, 'config']:
        return Response(response = json.dumps({ "result": False, "comment": "Invalid endpoint"} ),
                        status = 200, mimetype = 'application/json')

    if request.data:
        data = request.json
        if not ( isinstance(data, list) or isinstance(data, dict) ):
            return Response(response = json.dumps({ "result": False, "comment": "Invalid input data" }),
                            status = 400, mimetype = 'application/json')

    if request.method in ['POST', 'PUT', 'DELETE']:
        if not request.data:
            return Response(response = json.dumps({ "result": False, "comment": "No input data" }),
                            status = 400, mimetype = 'application/json')

    status = 200

    if request.method == 'GET':
        if request.data:
            if top_id == 'project':
                response = netdb.newColumn(column).project(data).fetch()
            else:
                response = netdb.newColumn(column).filter(data).fetch()

        # device and interface columns do not need config builders.
        elif column not in ['device', 'interface'] and opt == 'config':
            response = builder.newBuilder(column, top_id).build()
        else:
            response = netdb.newColumn(column).filter(top_id).fetch()

    # POST / PUT methods supported for 'validate' endpoint only, not
    #     supported for regulare (i.e. device / set id) top_ids.
    elif request.method == 'POST':
        if top_id == 'validate':
            response = netdb.newColumn(column).set(data).validate()
        elif not top_id:
            response = netdb.newColumn(column).set(data).save()
        else:
            status = 400

    elif request.method == 'PUT':
        if top_id == 'validate':
            response = netdb.newColumn(column).set(data).validate()
        elif not top_id:
            response = netdb.newColumn(column).set(data).update()
        else:
            status = 400

    elif request.method == 'DELETE':
        response = netdb.newColumn(column).filter(data).delete()

    else:
        status = 400

    if status == 400:
        response = {"result": False, "comment": "Invalid method"}

    return Response(response = json.dumps(response), status = status, mimetype = 'application/json')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
