#!/usr/bin/env python3
"""
Hash a password using bcrypt
"""
import bcrypt
from typing import Optional, Union


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt

    Args:
      - password(str): The input password

    Returns:
      - Bytes: The salted hash of the input password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
