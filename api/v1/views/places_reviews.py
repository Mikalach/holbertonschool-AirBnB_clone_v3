#!/usr/bin/python3
"""Defines the RESTful API actions for the user objects."""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_all_reviews(place_id):
    """Retrieves the list of all Reviews objects."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}, 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_place(place_id):
    """Creates a review object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    user_id = data.get('user_id')
    if user_id is None:
        abort(400, 'Missing user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    text = data.get('text')
    if text is None:
        abort(400, 'Missing text')
    data['place_id'] = place_id
    data['user_id'] = user_id
    data['text'] = text
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
