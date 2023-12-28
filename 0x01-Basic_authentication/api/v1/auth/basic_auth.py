#!/usr/bin/env python3
"""
The basic auth class.
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    Class auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        This method extract the Base64 part of the authorization header
        for basic authentication.

        Args:
          - Authorization_header (str): Authorization header to extract from.

        Returns:
          - str: Base64 part of the authorization header, or None.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        # Extracting value after "Basic ", 'with a space at the end'.
        base64_part = authorization_header[len("Basic "):]
        return base64_part

    def instance_classes(self):
        """
        This method creates instance of some methods for us to use in this
        class.
        """
        auth = Auth()
        authorization_header = auth.authorization_header(request)

    def decode_base64_authorization_header(self,
                                           authorization_header: str) -> str:
        """
        Decode the base64 string and return thr decoded value as "utf-8"
        string.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None

        try:
            decoded_byte = base64.b64decode(authorization_header)
            # Coverts decoded bytes to utf-8 string
            decoded_value = decoded_byte.decode('utf-8')
            return decoded_value
        except base64.binascii.Error:
            # Handle cases when the input is not a valid base64 string
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract user email, password from the base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the decoded values into email, password using ':'
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return the User instance based on email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the User instance in the database based on email
        users = User.search({'email': user_email})
        if not users:
            return None

        # Check if the provided password is valid for any of the found users
        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        # If no matching user with valid password is found, return None
        return None
