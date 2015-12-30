#! /usr/bin/env python
# coding=utf8

import json
from flask import \
    Flask, \
    render_template


app = Flask(__name__, static_folder='assets', template_folder='tmpl')
app.secret_key = open('secret').read()


@app.route('/')
def index():
    resp = \
        render_template(
            'index.html',
            ad_url=config['ad_url']),
    return resp


if __name__ == '__main__':
    global config
    config = json.load(open('config.json'))
    app.run(host='0.0.0.0', port=config['port'])
