#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from .index import *
from .users import *
from .session_auth import session_auth_views

User.load_from_file()

# Add new view to the blueprint
app_views.register_blueprint(session_auth_views)
