#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.auth import auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
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
    elif auth_type == "session_auth":
        # Create an instance of SessionAuth if AUTH_TYPE is session_auth
        auth = SessionAuth()
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
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/', '/api/v1/auth_session/login/']

    # If the request path is not in the excluded_path, check for
    # authentication
    if (request.path not in excluded_paths and
            auth.require_auth(request.path, excluded_paths)):

        # Checking if both authorization header and session cookie are missing
        # return 401 error.
        if (auth.authorization_header(request) is None and
                auth.session_cookie(request)) is None:
            abort(401)

        # Assign the result of auth.current_user(request) to
        # request.current_user
        request.current_user = auth.current_user(request)

        # Checking if current user returns None, return 403 error.
        if request.current_user is None:
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
