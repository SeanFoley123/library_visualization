"""
A Flask server that presents a minimal browsable interface for the Olin course catalog.

author: Oliver Steele <oliver.steele@olin.edu>
date  : 2017-01-18
license: MIT
"""
import os
import json

from flask import Flask, redirect, render_template, request, url_for

from api import search


app = Flask(__name__)


@app.route('/health')
def health():
    return 'ok'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=["POST"])
def query_api():
    query_string = request.form.get("query")
    return json.dumps(search(query_string))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = "127.0.0.1" if port == 5000 else "0.0.0.0"
    app.run(host=host, debug=True, port=port)
