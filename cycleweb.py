#!/usr/bin/python3
from cycledetect import CycleDetect
from flask import Flask, request
import flask
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


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
        d = request.get_json()
        f = StringIO(d['data'])
        cycles = cd.run(f)
        return cd.format(cycles)


if __name__ == '__main__':
    app.debug=True
    app.run()


