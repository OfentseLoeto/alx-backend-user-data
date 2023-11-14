#!/usr/bin/env python3
"""
The basic auth class.
"""
from api.v1.auth.auth import Auth
import base64


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

    def extract_user_credentials(self,
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
