import os
import json

from flask import Flask, redirect, render_template, request, url_for

from api import search, create_forest


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
    search_results = search(query_string)
    return json.dumps(create_forest(search_results))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = "127.0.0.1" if port == 5000 else "0.0.0.0"
    app.run(host=host, debug=True, port=port)
