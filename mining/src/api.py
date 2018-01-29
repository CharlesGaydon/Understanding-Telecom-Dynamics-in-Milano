from flask import Flask, render_template
from flask_restful import Resource, Api
import json
from mining.src.model.mining import *


app = Flask(__name__)
api = Api(app)


class Clustering(Resource):
    def get(self, algo):
        clustering = ClusteringResult(5)

        # /home/enzoclustering.get_apriori_result()
        d = {}
        if algo == 'kmeans':
            d = clustering.get_kmeans_result(5)
        if algo == 'tree':
            d = clustering.get_isolation_forest_result()
        if algo == 'dbscan':
            d = clustering.get_DBSCAN_result()
        if algo == 'ward':
            d = clustering.get_hierarchical_result()
        if algo == 'charles':
            files = [
                'clusters_DBSCAN_eps_5.75_min_1.json',
                'clusters_DBSCAN_eps_5.75_min_7.json',
                'clusters_DBSCAN_eps_5.75_min_3.json',
                'clusters_DBSCAN_eps_5.75_min_9.json',
                'clusters_DBSCAN_eps_5.75_min_5.json'
            ]
            d = []
            for file_ in files:
                dd = json.load(open('learning/data/DBSCAN_json_clusters/' + file_))['Cluster']
                d.append(dict(list(map(lambda x: (x[0], x[1] + 1), dd.items()))))
        data = json.dumps(d)
        return data


@app.route('/')
def show_basic():
    return render_template("index.html")


api.add_resource(Clustering, '/<string:algo>')


def run():
    app.run(debug=True)