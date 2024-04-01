#!/usr/bin/python3
"""Create a new view for State objects"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities():
    """Get all Amenities"""
    resp = [
        amenity.to_dict() for amenity in storage.all(Amenity).values()
    ]
    return jsonify(resp)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenities_by_id(amenity_id):
    """Get Amenities by id"""
    resp = storage.get(Amenity, amenity_id)
    if resp is None:
        abort(404)
    return jsonify(resp.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    """Delete Amenities"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def insert_amenities():
    """Insert Amenities"""
    tr = request.get_json()
    if type(tr) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in tr:
        return abort(400, {'message': 'Missing name'})
    new_amenities = Amenity(**tr)
    new_amenities.save()
    return jsonify(new_amenities.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenities(amenity_id):
    """Update Amenities"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    tr = request.get_json()
    if type(tr) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for k, v in tr.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict()), 200
