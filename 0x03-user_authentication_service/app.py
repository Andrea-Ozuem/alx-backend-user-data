#!/usr/bin/env python3
'Flask app module'

from flask import Flask, jsonofy, request

app = Flask(__name__)


def index('/', strict_slashes=False) -> str:
    '''return a JSON payload of the form'''
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
