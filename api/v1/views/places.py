#!/usr/bin/python3
"""Defines the RESTful API actions for the place objects."""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_all_places():
    """Retrieves the list of all place objects."""
    amenities = storage.all(Place).values()
    return jsonify([place.to_dict() for place in amenities])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places', methods=['POST'], strict_slashes=False)
def create_place():
    """Creates a place object."""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    id = data.get('user_id')
    if id is None:
        abort(400, 'Missing user_id')
    if id is not isinstance(User):
        abort(404)
    name = data.get('name')
    if name is None:
        abort(400, 'Missing name')
    place = place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'city_id', 'create_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200 
