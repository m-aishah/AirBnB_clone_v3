#!/usr/bin/python3
""" Returns the API status """

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def route_status():
    # returns the route status in json
    return jsonify({
        "status": "OK"
        })
