import os

from collections import defaultdict

from flask import Flask, render_template, request, flash, redirect
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

UPLOAD_FOLDER = '/Users/eabell/tmp'

def read_file(filename):
    df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename), sep='\t', header=None, names=['state', 'town', 'pop'], skiprows=1)
    list_of_pops = list(df['pop'])
    return(list_of_pops)

def create_plot():
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y})

    data = [
        go.Bar(
            x=df['x'],
            y=df['y'],
        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    print(graphJSON)
    return graphJSON

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    bar = create_plot()
    return render_template('index.html', plot=bar)

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        list_of_pops = read_file(filename)
        freq = defaultdict(int)
        for number in list_of_pops:
            try:
                first_digit = int(str(number)[0])
            except Exception:
                continue
            freq[first_digit] += 1
        data = [
            go.Bar(
                x=list(freq.keys()),
                y=list(freq.values())
            )
        ]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        flash('File successfully uploaded: {} with {} pops'.format(filename, len(list_of_pops)))
        return render_template('index.html', plot=graphJSON)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
