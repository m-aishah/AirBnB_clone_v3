#!/usr/bin/python3
"""
A new view for State objects that handles all default RESTFul API actions
"""

from flask import Flask, jsonify, request
from models import storage
from api.v1.views import app_views
from models.state import State


app = Flask(__name__)


@app_views.route('/states', methods=['GET'])
def get_all_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def add_state():
    """Adds/Creates a new State object"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**data)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update the State object with all key-value pairs of the dictionary"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
