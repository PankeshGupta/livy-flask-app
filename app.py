from flask import Flask, send_file, request, jsonify
from flask_restful import Resource, Api
from flask_restful import reqparse
from livy.client import HttpClient
from urlparse import urlparse
import service

global kdensity_response
kdensity_response = None

app = Flask(__name__, static_folder="static")
api = Api(app)
client = HttpClient(urlparse("http://172.16.2.72:8998"), load_defaults=False)
service.set_client(client)
service.upload_jar_files()



class KernelDensityInput(Resource):
    def post(self):
        global kdensity_response
        print "Inside post of Kerneldenisty"
        parser = reqparse.RequestParser()
        parser.add_argument('column', type=str, help='Column name')
        parser.add_argument('bandwidth', type=str, help='Value for bandwidth')
        parser.add_argument('points', type=str, help='Value for points list')
        args = parser.parse_args()

        _column = args['column']
        _bandwidth = args['bandwidth']
        _points = args['points']
        print "column::", _column
        print "_bandwidth::", _bandwidth
        print "_points::", _points
        response = service.process_kdensity_request(_column, _bandwidth, _points)
        kdensity_response = response
        return jsonify(estimationPoints=response[0],
                       results=response[1])

    def get(self):
        return send_file("static/html/kdensity.html")

class KernelDensityResult(Resource):
    def post(self):
        global kdensity_response
        return jsonify(estimationPoints=kdensity_response[0],
                       results=kdensity_response[1])

    def get(self):
        return send_file("static/html/kdensityresult.html")

@app.route('/', methods=['GET', 'POST'])
def index():
    return send_file("static/html/index.html")


@app.route('/home', methods=['GET'])
def home():
    return send_file("static/html/home.html")


# @app.route('/kdensity', methods=['GET', 'POST'])
# def kdensity():
#     if request.method == 'GET':
#         return send_file("static/html/kdensity.html")
#     else:
#         pass


api.add_resource(KernelDensityInput, '/kdensity')
api.add_resource(KernelDensityResult, '/kdensity/result')

if __name__ == "__main__":
    app.run(host='0.0.0.0')