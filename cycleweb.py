#!/usr/bin/python3
from cycledetect import CycleDetect
from flask import Flask, request
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


app = Flask(__name__)

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/cycle", methods=['GET', 'POST'])
def cycle():
    if request.method == 'POST':
        cd = CycleDetect()
        f = StringIO(request.form['data'])
        cycles = cd.run(f)
        return cd.format(cycles)


if __name__ == '__main__':
    app.debug=True
    app.run()


