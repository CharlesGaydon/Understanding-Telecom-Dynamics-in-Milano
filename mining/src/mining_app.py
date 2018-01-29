from flask import Flask, render_template, Response, make_response
import json
from mining.src.model.mining import *

app = Flask(__name__)

@app.route('/<algo>')
def show_basic(algo):
    if algo == 'kmeans':
        d = get_kmeans_result(5)
    elif algo == 'dbscan':
        d = get_DBSCAN_result()
    else:
        d = get_apriori_result(32,50,32,50,5)
    data = json.dumps(d)
    return render_template("index.html", data=data)


@app.route('/')
def main():
    return "hello world"

def run():
    app.run(threaded=True, host='0.0.0.0')
