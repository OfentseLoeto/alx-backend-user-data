#!/usr/bin/env python3
"""
Hashing a password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash and salt the given password using bcrypt.

    Arguments:
    - password (str): The password to be hashed.

    Returns:
    - bytes: The salted and hashed password.
    """
    # Generate a random salt and hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hashed_password
