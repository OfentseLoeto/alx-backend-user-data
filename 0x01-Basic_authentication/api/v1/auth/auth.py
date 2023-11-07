#!/usr/bin/env python3
"""
Implemetation of an Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.

        Args:
          - Path (str): The path to be checked for authentication
          - excluded_paths (List[str]): List of paths that are excluded from
            authentication

        Returns:
          - bool: True if authentication is required, False otherwise
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        # Ensure that path end with trailing slash for accurate matching.
        if path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if path.startswith(excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the value of the Authorization header.
        Args:
          - request: Flask request object

        returns:
          - str: Value of the Authorization header if it exist, or None.
        """
        if request is None:
            return None
        auth_header = request_headers.get("Authorization")
        if not auth_header:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        User method that return none
        """
        return None
