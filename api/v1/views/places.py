#!/usr/bin/python3
"""implement a rule return a view"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from flasgger.utils import swag_from


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def places_city(city_id):
    """return place object by city"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    return jsonify([place.to_dict() for place in cities.places])


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def show_places(place_id):
    """return a Place object"""
    plc = storage.get(Place, place_id)
    if plc is None:
        abort(404)
    return jsonify(plc.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from('documentation/place/del_place.yml', methods=['DELETE'])
def del_place(place_id):
    """delete a Place object"""
    plc = storage.get(Place, place_id)
    if plc is None:
        abort(404)
    plc.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def inst_place(city_id):
    """insert a Place object"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    resp = request.get_json()
    if type(resp) != dict:
        abort(400, description="Not a JSON")
    if not resp.get("user_id"):
        abort(400, description="Missing user_id")
    users = storage.get(User, res.get("user_id"))
    if users is None:
        abort(404)
    if not resp.get("name"):
        abort(400, description="Missing name")
    new_place = Place(**resp)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def place_search():
    """Retrieves all Place objects"""
    tr = request.get_json()
    if type(tr) != dict:
        abort(400, description="Not a JSON")
    id_states = tr.get("states", [])
    id_cities = tr.get("cities", [])
    id_amenities = tr.get("amenities", [])
    places = []
    if id_states == id_cities == []:
        places = storage.all(Place).values()
    else:
        states = [
            storage.get(State, _id) for _id in id_states
            if storage.get(State, _id)
        ]
        cities = [city for state in states for city in state.cities]
        cities += [
            storage.get(City, _id) for _id in id_cities
            if storage.get(City, _id)
        ]
        cities = list(set(cities))
        places = [place for city in cities for place in city.places]

    amenities = [
        storage.get(Amenity, _id) for _id in id_amenities
        if storage.get(Amenity, _id)
    ]

    resp = []
    for place in places:
        resp.append(place.to_dict())
        for amenity in amenities:
            if amenity not in place.amenities:
                resp.pop()
                break

    return jsonify(resp)


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
@swag_from('documentation/place/post_sch.yml', methods=['POST'])
def update_place(place_id):
    """update a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    resp = request.get_json()
    if type(resp) != dict:
        abort(400, description="Not a JSON")
    for k, v in resp.items():
        if k not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
