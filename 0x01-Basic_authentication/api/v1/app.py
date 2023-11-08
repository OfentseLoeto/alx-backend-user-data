#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
# Initialize Auth to None
auth = None

# Load the right instance of Authentication
# based on the environmental variable Auth_type
auth_type = getenv("AUTH_TYPE")

if auth_type:
    if auth_type == "basic_auth":
        # Create an instance of basic_auth if auth_type is basic_auth.
        auth = BasicAuth()
    else:
        # If AUTH_TYPE is not basic_auth, use Auth
        from api.v1.auth.auth import Auth
        auth = Auth()


@app.before_request
def before_request():
    """
    Handler for the before request
    """
    if auth is None:
        return

    # List of paths that don't require authentication.
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/'
                      ]
    # If the request path is not in the excluded_path, check for
    # authentication.
    if (request.path not in excluded_paths and auth.require_auth(request.path, excluded_paths)):

        # Checking if authorization header is missing and
        # 404 error.
        if auth.authorization_header(request) is None:
            abort(401)

        # Checkinf if current user returns Non
        if auth.current_user(request) is None:
            abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Unauthorized handler

    returns:
      - status_code 401
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Forbidden handler

    returns:
      - 403 status_code.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
