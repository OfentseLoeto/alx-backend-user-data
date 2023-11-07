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
        Require auth
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Authorization method
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        User method that return none
        """
        return None
