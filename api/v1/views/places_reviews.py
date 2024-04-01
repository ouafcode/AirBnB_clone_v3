#!/usr/bin/python3
"""return a view"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from flasgger.utils import swag_from


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_reviews.yml', methods=['GET'])
def reviews_place(place_id):
    """return Review objects by Place"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    return jsonify([review.to_dict() for review in places.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_review.yml', methods=['GET'])
def sh_review(review_id):
    """return a Review object"""
    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)
    return jsonify(rev.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from('documentation/reviews/del_reviews.yml', methods=['DELETE'])
def del_review(review_id):
    """delete a Review object"""
    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)
    rev.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/reviews/post_reviews.yml', methods=['POST'])
def ins_review(place_id):
    """insert a Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    resp = request.get_json()
    if type(resp) != dict:
        abort(400, description="Not a JSON")
    if not resp.get("user_id"):
        abort(400, description="Missing user_id")
    resp['place_id'] = place_id
    user = storage.get(User, resp.get('user_id'))
    if user is None:
        abort(404)
    if not resp.get("text"):
        abort(400, description="Missing text")
    new_review = Review(**resp)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
@swag_from('documentation/reviews/put_reviews.yml', methods=['PUT'])
def upd_review(review_id):
    """update a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    resp = request.get_json()
    if type(resp) != dict:
        abort(400, description="Not a JSON")
    for k, val in resp.items():
        if k not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 200
