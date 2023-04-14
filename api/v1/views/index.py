#!/usr/bin/python3
"""
module documented
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    stats = {}
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    for cls, name in classes.items():
        count = storage.count(cls)
        stats[name] = count
    return jsonify(stats)
