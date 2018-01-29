from flask import Flask, render_template
from flask_restful import Resource, Api
import json
from mining.src.model.mining import *


app = Flask(__name__)
api = Api(app)


class Clustering(Resource):
    def get(self, algo):
        if algo == 'kmeans':
            d = get_kmeans_result(5)
        elif algo == 'tree':
            d = get_isolation_forest_result()
        else:
            d = get_DBSCAN_result()
        data = json.dumps(d)
        return data


@app.route('/')
def show_basic():
    return render_template("index.html")


api.add_resource(Clustering, '/<string:algo>')


def run():
    app.run(debug=True)