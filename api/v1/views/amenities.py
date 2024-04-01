#!/usr/bin/python3
"""Create a new view for State objects"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/amenity/all_amenity.yml')
def amenity():
    """Get amenity"""
    resp = [
        amenity.to_dict() for amenity in storage.all(Amenity).values()
    ]
    return jsonify(resp)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/amenity/get_amenity.yml', methods=['GET'])
def amenity_id(amenity_id):
    """Get Amenities by id"""
    resp = storage.get(Amenity, amenity_id)
    if resp is None:
        abort(404)
    return jsonify(resp.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/amenity/del_amenity.yml', methods=['DELETE'])
def del_amenity(amenity_id):
    """Delete Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/amenity/post_amenity.yml', methods=['POST'])
def insert_amenity():
    """Insert Amenity"""
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
@swag_from('documentation/amenity/put_amenity.yml', methods=['PUT'])
def update_amenity(amenity_id):
    """Update Amenity"""
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
