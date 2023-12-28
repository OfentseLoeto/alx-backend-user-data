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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate that the provided password matches the hashed password using
    bcrypt.

    Arguments:
    - hashed_password (bytes): The hashed password stored in the database.
    - password (str): The plaintext password to be validated.

    Returns:
    - bool: True if the password is valid, False otherwise.
    """
    # Use bcrypt to check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
