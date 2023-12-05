#!/usr/bin/python3
"""
A new view for City objects that handles all default RESTFul API actions
"""

from flask import Flask, jsonify, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City


app = Flask(__name__)


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a state"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Adds/Creates a new City object"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_city = City(**data)
    new_city.state_id = state.id
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ('id', 'state_id', 'created_at', 'updated_at'):
            setattr(city, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
