#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.auth import auth
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
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
        auth = Auth()


@app.before_request
def before_request():
    """
    Handler for the before request
    """
    if auth is None:
        return

    # List of paths that don't require authentication.
    excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/'
    ]

    # If the request path is not in the excluded_path, check
    # for authentication.
    if (request.path not in excluded_paths and
            auth.require_auth(request.path, excluded_paths)):

        # Checking if authorization header is missing and 404 error.
        authorization_header = auth.authorization_header(request)

        # Checking if authorization header is missing and 401 error.
        if auth.authorization_header(request) is None:
            print("Authorization header is missing. Aborting with 401.")
            abort(401)

        # Assign the result of auth.current_user(request) to
        # request.current_user
        current_user = auth.current_user(request)
        request.current_user = current_user

        print(f"Authorization header: {authorization_header}")
        print(f"Current user: {current_user}")

        # Checking if current_user is None
        if request.current_user is None:
            print("Current user is None. Aborting with 403.")
            abort(403)


@app.errorhandler(404)
def not_found(error):
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """ Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
