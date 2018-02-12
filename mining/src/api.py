from flask import Flask, render_template
from flask_restful import Resource, Api
import json
from mining.src.model.mining import *
from flask_bootstrap import Bootstrap

app = Flask(__name__)
# Bootstrap(app)

api = Api(app)

clustering = ClusteringResult(5)


class Clustering(Resource):
    def get(self, algo, cluster=4):
        d = {}
        if algo == 'apriori':
            # caution wet floor
            d = {}
            pass
            # d = clustering.apply_apriori('SMSin')
        if algo == 'kmeans':
            d = clustering.get_kmeans_result(cluster)
        if algo == 'tree':
            d = clustering.get_isolation_forest_result()
        if algo == 'dbscan':
            d = clustering.get_DBSCAN_result()
        if algo == 'ward':
            d = clustering.get_hierarchical_result()
        data = json.dumps(d)
        return data


@app.route('/')
def show_basic():
    return render_template("index.html")


@app.route('/rapport')
def show_rapport():
    return render_template("rapport.html")



api.add_resource(Clustering, '/<string:algo>', '/<string:algo>/<int:cluster>')


def run():
    app.run(debug=True)