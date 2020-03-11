from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

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

@app.route('/')
def index():
    bar = create_plot()
    return render_template('index.html', plot=bar)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
