#!/usr/bin/env python3
"""
Db module

This module provides a DB class for interacting with the database.
"""
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from user import Base, User


class DB:
    """
    The database class

    This class represents the database interaction and provides
    methods for data manipulation.

    Attributes:
      _ engine: SQLAlchemy engine for database connection
      _ session: SQLAlchemy session for database interaction

    """
    Session = sessionmaker()

    def __init__(self) -> None:
        """
        Initialize a new db instace
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add user to the database

        Args:
          - email(str): User's email
          - hashed_password: User's hashed_password

        Return:
          - Created user object
        """
        session = self._session
        # Create a new User instance.
        user = User(email=email, hashed_password=hashed_password)

        # Add a new user to the session.
        self._session.add(user)

        # Commit changes to the database
        self._session.commit()

        # Return the created user object
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by specified filter criteria

        Args:
          - **kwargs: Arbitrary keyword arguments for filtering

        Returns:
          - User: The first User object found

        Raises:
          -  NoResultFound: If no result is found
          - InvalidRequestError: If an invalid request is made
        """

        try:
            return self._session.query(User).filter_by(**kwargs).one()

        except NoResultFound:
            raise NoResultFound("No user found")

        except InvalidRequestError:
            raise InvalidRequestError("Invalid request")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes based on the provided arguments

        Args:
            user_id (int): User's ID
            **kwargs: Arbitrary keyword arguments for updating user attributes

        Raises:
            NoResultFound: If no user is found with the given user_id
            ValueError: If an invalid attribute is provided
        """
        user = self.find_user_by(id=user_id)
        if not user:
            raise NoResultFound("User not found")

        # Update user attributes
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")

        # Commit changes to the database
        self._session.commit()
