#!/usr/bin/env python3
"""
Implemetation of an Auth class
"""

from flask import Request
from os import getenv
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class provides basic authentication functionalities.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.

        Args:
          - path (str): The path to be checked for authentication.
          - excluded_paths (List[str]): List of paths that are excluded
            from authentication.

        Returns:
          - bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        # Ensure that path ends with a trailing slash for accurate matching.
        path_with_slash = path if path.endswith('/') else path + '/'
        excluded_paths = [
                p if p.endswith('/') else p + '/' for p in excluded_paths
                ]
        return path_with_slash not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Get the value of the Authorization header.

        Args:
          - request: Flask request object.

        Returns:
          - str: Value of the Authorization header if it exists, or None.
        """
        if request is None:
            return None
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method that returns None.

        Args:
          - request: Flask request object.

        Returns:
          - None
        """
        return None

    def session_cookie(self, request: Request = None) -> str:
        """
        Return the value of the cookie named _my_session_id from the request.

        Args:
          - request (Request): Flask Request object.

        Returns:
          - str: Cookie value or None if request is None or the cookie is
                 not present.
        """
        if request is None:
            return None

        session_name = getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name, None)
