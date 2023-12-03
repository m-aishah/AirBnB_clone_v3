#!/usr/bin/python3
""" Returns the API status """

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def route_status():
    # returns the route status in json
    return jsonify({
        "status": "OK"
        })


@app_views.route('/stats')
def object_no():
    # returns the number of objects by type
    all_objects = storage.all()

    # if not all_objects:
    #    return jsonify({"error": "No objects found in storage"}), 404
    all_types = [obj.__class__.__name__ for obj in all_objects.values()]
    counts = {type_: storage.count(type_) for type_ in all_types}
    return jsonify(counts)
