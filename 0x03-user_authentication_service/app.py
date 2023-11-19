#!/usr/bin/env python3
'Flask app module'

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index() -> str:
    '''return a JSON payload of the form'''
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
