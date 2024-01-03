#!/usr/bin/env python3
"""
Module for Session Authentication view
"""
from flask import Blueprint, abort, jsonify, request
from models.user import User
from api.v1.app import auth

session_auth_views = Blueprint('session_auth_views', __name__)


@session_auth_views.route(
        '/auth_session/login', methods=['POST'], strict_slashes=False
        )
def login() -> str:
    """
    Handles POST request to /auth_session/login
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)

    response_json = user.to_json()
    response = jsonify(response_json)
    response.set_cookie(auth.session_name, session_id)

    return response


@session_auth_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=False
        )
def logout() -> str:
    """
    Handles DELETE request to /auth_session/logout
    """
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({})
