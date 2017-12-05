from flask import Flask, render_template, Response,make_response
 
import redis
import random
import json
import pandas
import numpy as np
from webapp.model.prediction_during_time import get_callin_during_time


df = get_callin_during_time('data/sms.csv')
 
d = [
    dict([
        (colname, row[i])
        for i,colname in enumerate(df.columns)
    ])
    for row in df.values
]
app = Flask(__name__)
 
@app.route('/streamdata')
def event_stream():
    make_response(d.to_json())
 
@app.route('/')
def show_basic():
    x = random.randint(0,101)
    y = random.randint(0,101)
    print(json.dumps(d))
    return render_template("visu.html",data=json.dumps(d))
 
 
def run():
    app.run(threaded=True,
    host='0.0.0.0'
)
