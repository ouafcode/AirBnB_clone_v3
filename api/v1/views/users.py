#!/usr/bin/python3
"""Create a view for user object"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/user/users_all.yml', methods=['GET'])
def users():
    """get stored users"""
    resp = [
        user.to_dict() for user in storage.all(User).values()
    ]
    return jsonify(resp)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/user/get_users.yml', methods=['GET'])
def user_id(user_id):
    """get a user  by id"""
    resp = storage.get(User, user_id)
    if resp is None:
        abort(404)
    return jsonify(resp.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/del_users.yml', methods=['DELETE'])
def del_user(user_id):
    """Delete user by id """
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    users.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/user/post_users.yml', methods=['POST'])
def insert_user():
    """Insert user object"""
    tr = request.get_json()
    if type(tr) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'email' not in tr:
        return abort(400, {'message': 'Missing email'})
    if 'password' not in tr:
        return abort(400, {'message': 'Missing password'})
    new_user = User(**tr)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/user/put_users.yml', methods=['PUT'])
def update_user_by_id(user_id):
    """update user object"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    tr = request.get_json()
    if type(tr) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for k, v in tr.items():
        if k not in ["id", "email", "created_at", "updated_at"]:
            setattr(users, k, v)
    storage.save()
    return jsonify(users.to_dict()), 200
