#!/usr/bin/python3

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import io
from flask import Flask, request, jsonify
import flask
from cycledetect import CycleDetect

app = Flask(__name__, static_folder='cycleweb-react/build/static',
            static_url_path='/static')

@app.route("/")
def root():
    return flask.send_from_directory('cycleweb-react/build',
                                     'index.html')

@app.route("/cycle", methods=['GET', 'POST'])
def cycle():
    if request.method == 'POST':
        cd = CycleDetect()
        if 'file' in request.files:
            f = io.TextIOWrapper(request.files['file'])
        else:
            d = request.get_json()
            f = StringIO(d['data'])
        return jsonify({'result': cd.run(f)})

if __name__ == '__main__':
    app.debug = True
    app.run()


