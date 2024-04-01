#!/usr/bin/python3
"""Create a new view for State objects """
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_stats.yml', methods=['GET'])
def get_states():
    my_dict = []
    for value in storage.all(State).values():
        my_dict.append(value.to_dict())
    return jsonify(my_dict)


@app_views.route('/states/<path:state_id>')
@swag_from('documentation/state/get_stats.yml', methods=['GET'])
def get_stats(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<path:state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/del_stats.yml', methods=['DELETE'])
def delete_stats(state_id):
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/state/post_stats.yml', methods=['POST'])
def post_stats():
    resp = request.get_json()
    if type(resp) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in resp:
        return abort(400, {'message': 'Missing name'})
    new_state = State(**resp)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<path:state_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/state/put_stats.yml', methods=['PUT'])
def put_stats(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    resp = request.get_json()
    if type(resp) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for k, v in resp.items():
        if k not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
