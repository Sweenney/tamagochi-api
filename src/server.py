#!/usr/bin/env python3
import argparse

from flask import Flask
from flask_cors import CORS

import os
import json

from game import Game

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--oneshot', help='generate game with http server', action="store_true")
args = parser.parse_args()

app = Flask(__name__)
CORS(app)

g = None

@app.route('/')
def game():
    if g:
        ret = {
            'characters': g.to_json(),
            'simulation_time': (g.simulation_time_end - g.simulation_time_start) * 1000
        }
        return json.dumps(ret)
    else:
        return ('', 503)

@app.route('/set')
def set_game():
    if g and g.has_ended:
        if request.args.get('characters'):
            g.characters_count = request.args.get('characters', 50)
        return ('', 200)
    else:
        return ('', 503)

@app.route('/reset')
def reset():
    if g and g.has_ended:
        g.reset()
        return ('', 200)
    else:
        return ('', 503)

if __name__ == '__main__':
    if not args.oneshot:
        app.run(host='0.0.0.0', debug=True)
    g = Game()
