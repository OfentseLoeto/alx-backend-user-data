#!/usr/bin/env python3
"""
Db module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import User
from user import Base


class DB:
    """
    The database class
    """
    def __init__(self) -> None:
        """
        Initialize a new db instace
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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

    def add_user(self, email, hashed_password):
        """
        Add user to the database
        """

        # Create a new User instance.
        new_user = User(email=email, hashed_password=hashed_password)

        # Add a new user to the session.
        self._session.add(new_user)

        # Commit changes to the database
        self._session.commit()

        # Return the created user object
        return new_user
