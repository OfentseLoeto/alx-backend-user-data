#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/users", methods=["POST"])
def register_user():
    """
    The App returns a message.
    """
    try:
        email = request.form["email"]
        password = request.form["password"]

        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})

    except ValueError as e:
        return jsonify({"message": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
