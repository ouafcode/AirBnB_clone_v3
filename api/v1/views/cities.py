#!/usr/bin/python3
"""This module implement a rule that return a view"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State
from flasgger.utils import swag_from


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/city/city_state.yml', methods=['GET'])
def city_state(state_id):
    """return city objects by state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def show_city(city_id):
    """return a City object"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    return jsonify(cities.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from('documentation/city/del_city.yml', methods=['DELETE'])
def del_city(city_id):
    """delete a City object"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    cities.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/city/post_city.yml', methods=['POST'])
def insert_cities(state_id):
    """insert a City object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    resp = request.get_json()
    if type(resp) != dict:
        abort(400, description="Not a JSON")
    if not resp.get("name"):
        abort(400, description="Missing name")
    new_cities = City(**resp)
    new_cities.state_id = state_id
    new_cities.save()
    return jsonify(new_cities.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def update_cities(city_id):
    """update a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    resp = request.get_json()
    if type(resp) != dict:
        abort(400, description="Not a JSON")
    for k, v in resp.items():
        if k not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 200
