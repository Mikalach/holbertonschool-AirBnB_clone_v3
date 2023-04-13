#!/usr/bin/python3
"""Defines the RESTful API actions for the place objects."""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    from models.city import City
    from models.place import Place
    """Retrieves the list of all place objects."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all(Place).values()
    cities = [city.to_dict() for city in places.cities]
    return jsonify(cities)


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


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place():
    from models.city import City
    """Creates a place object."""
    data = request.get_json()
    city_id = data.get('city_id')
    if city_id is not isinstance(City):
        abort(404)
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
