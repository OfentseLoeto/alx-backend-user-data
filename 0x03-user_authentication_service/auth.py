#!/usr/bin/env python3
"""
Hash a password using bcrypt
"""
import bcrypt
from typing import Optional, Union
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """
    Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

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

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user

        Args:
          - email(str): User's email
          - password(str): User's password

        Returns:
          - User: The created user object

        Raises:
          - ValueError: If the user with thegiven email already exists.
        """
        try:
            # Checks if a user with the given email already exists using the
            # find_user_by method from the DB class
            existing_user = self._db.find_user_by(email=email)

            # If a user is found it raises a ValueError
            if existing_user:
                raise ValueError(f"User {email} already exists")

        except NoResultFound:
            hashed_password = self._hashed_password(password)
            user = self._db.add_user(email, hashed_password)

            # returns the created User object.
            return user
