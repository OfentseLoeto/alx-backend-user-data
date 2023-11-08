#!/usr/bin/env python3
"""
The basic auth class.
"""
from api.v1.auth.auth import Auth


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
