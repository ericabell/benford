import os

from collections import defaultdict
from math import log
from scipy.stats import chisquare

from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

UPLOAD_FOLDER = '/Users/eabell/tmp'

BENFORDS_LAW = {d: log(d+1, 10)-log(d, 10) for d in range(1, 10)}


def process_line(line):
    """
    Given: a line from input file
    Perform: split on whitespace and extract any string that passes int()
    Returns: list of numbers from the line
    """
    numbers = []
    for component in line.split():
        try:
            good_number = int(component)
        except ValueError:
            continue
        else:
            numbers.append(good_number)

    return numbers


def get_numbers_from_file(filename):
    """
    """
    numbers = []

    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
        lines = [line.rstrip() for line in f]

    for line in lines:
        try:
            numbers.extend(process_line(line))
        except Exception as e:
            print('{} -- {}'.format(e, line))
            continue

    return {'numbers': numbers, 'count': len(numbers)}


def generate_plot(filename):
    """
    Given: a filename in the UPLOADS_FOLDER
    Perform: extract numbers and construct graph
    Returns: json string representing the graph
    """
    # numbers_dict = get_numbers_from_file(filename)
    numbers_dict = get_numbers_from_file(filename)
    numbers_count = numbers_dict['count']

    freq = defaultdict(int)
    for number in numbers_dict['numbers']:
        try:
            first_digit = int(str(number)[0])
        except Exception as e:
            print(e)
            continue
        freq[first_digit] += 1

    freq_normalized = {k: v/numbers_count for k, v in freq.items()}

    data = go.Bar(
            x=list(freq_normalized.keys()),
            y=list(freq_normalized.values()),
            name=filename,
    )
    benford = go.Bar(
            x=list(BENFORDS_LAW.keys()),
            y=list(BENFORDS_LAW.values()),
            name="Benford's Law"
    )

    hyp_test = chisquare(list(freq_normalized.values()), list(BENFORDS_LAW.values()))

    if hyp_test.pvalue < 0.05:
        title = "{} is significantly different from Benford's Law".format(filename)
    else:
        title = "{} obeys Benford's Law".format(filename)

    layout = go.Layout(title=title, xaxis_title='Digit', yaxis_title='Frequency')
    figure = go.Figure()
    figure.add_trace(data)
    figure.add_trace(benford)
    figure.update_layout(layout)

    return json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)


app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/')
def index():
    return render_template('index.html', plot=None)


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File successfully uploaded: {}'.format(filename))
        return render_template('index.html', plot=generate_plot(filename))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
