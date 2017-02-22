"""
A Flask server that presents a minimal browsable interface for the Olin course catalog.

author: Oliver Steele <oliver.steele@olin.edu>
date  : 2017-01-18
license: MIT
"""
import os

from flask import Flask, redirect, render_template, request, url_for
import requests as r
from bs4 import BeautifulSoup


app = Flask(__name__)


@app.route('/health')
def health():
    return 'ok'


@app.route('/<search_string>')
def home_page(search_string):
    search_string = search_string.replace(' ', '+')
    url = 'https://olin.tind.io/search?ln=en&p=%s&f=&rm=wrd&ln=en&sf=&so=d&rg=100' % search_string
    soup = BeautifulSoup(r.get(url).content, 'html.parser')
    books = [a.getText().replace('\n', '') for a in soup.find_all('div', 'result-title')]
    return render_template('index.html', books=books)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = "127.0.0.1" if port == 5000 else "0.0.0.0"
    app.run(host=host, debug=True, port=port)
