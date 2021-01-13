import os
import sys

from functools import partial

import scipy
import scipy.stats
import numpy as np
import pandas as pd

from flask import Flask, request, send_from_directory, send_file, jsonify, request

app = Flask(__name__, static_folder='build', static_url_path='')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('build/static/', path)


@app.route('/')
def index():
    return send_file('build/index.html')

@app.route('/dist_list')
def dist_list():
    return jsonify(
        dists=['norm', 'expon', 'maxwell', 'logistic']
    )

@app.route('/generate', methods=['GET'])
def generate():
    loc = float(request.args['loc'])
    scale = float(request.args['scale'])
    dist = request.args['dist']
    fn = request.args['function']

    dist = getattr(scipy.stats, dist)
    statfn = None
    
    if fn == 'pdf':
        statfn = dist.pdf
    elif fn == 'cdf':
        statfn = dist.cdf
    else:
        raise ValueError('Only cdf or pdf allowed as functions')

    X = np.linspace(dist.ppf(0.01), dist.ppf(0.99), 100)
    Y = statfn(X, loc=loc, scale=scale)

    return jsonify(
        X = X.tolist(),
        Y = Y.tolist()
    )


if __name__ == '__main__':

    if '-nojs' not in sys.argv:
        os.system('npm run build')

    app.run(host='127.0.0.1', port=5000)