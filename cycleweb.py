#!/usr/bin/python3

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import io
from flask import Flask, request, jsonify, send_file
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
        if 'file[]' in request.files:
            f = [ io.TextIOWrapper(x) \
                  for x in request.files.getlist('file[]') ]
        else:
            d = request.get_json()
            f = [StringIO(d['data'])]
        result = cd.run(f)
        print(len(result))
        return jsonify({'result': result})

@app.route("/cycle-viz", methods=['GET', 'POST'])
def cycle_viz():
    if request.method == 'POST':
        cd = CycleDetect()
        if 'file[]' in request.files:
            f = [ io.TextIOWrapper(x) \
                  for x in request.files.getlist('file[]') ]
        else:
            d = request.get_json()
            f = [StringIO(d['data'])]
        d = cd.graphviz(f)
        return send_file(io.BytesIO(d),
                         mimetype='image/png')

if __name__ == '__main__':
    app.debug = True
    app.run()


