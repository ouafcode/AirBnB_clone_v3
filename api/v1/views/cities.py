#!/usr/bin/python3
"""This module implement a rule that return a view"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def cities_by_state(state_id):
    """return city objects by state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def show_cities(city_id):
    """return a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_cities(city_id):
    """delete a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def insert_cities(state_id):
    """insert a City object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        abort(400, description="Not a JSON")
    if not res.get("name"):
        abort(400, description="Missing name")
    new_cities = City(**res)
    new_cities.state_id = state_id
    new_cities.save()
    return jsonify(new_cities.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def update_cities(city_id):
    """update a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        abort(400, description="Not a JSON")
    for k, v in res.items():
        if k not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 200
