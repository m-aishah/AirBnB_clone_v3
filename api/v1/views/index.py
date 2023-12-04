#!/usr/bin/python3
""" Returns the API status """

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.engine import db_storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


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
#   if not all_objects:
#        return jsonify({"error": "No objects found in storage"}), 404
#    # all_types = [obj.__class__.__name__ for obj in all_objects.values()]
    # counts = {type_: storage.count(type_) for type_ in all_types}
    counts = {class_name[:-1].lower() + 'ies' if class_name.endswith('y')
              else class_name.lower() + 's': storage.count(cls)
              for class_name, cls in classes.items()}
    return jsonify(counts)
