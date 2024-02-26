#!/usr/bin/python3
"""Handles all default RESTFul API actions"""
from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/', methods=['GET', 'POST'])
def states():
    if request.method == 'GET':
        states = storage.all(State)
        return jsonify([state.to_dict() for state in states.values()])
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        state = State(**data)
        state.save()
        return jsonify(state.to_dict()), 201

@app_views.route('/states/<string:state_id>', methods=['GET', 'DELETE', 'PUT'])
def state(state_id):
    states = storage.get(State, state_id)
    if not states:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for key, value in request.json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
