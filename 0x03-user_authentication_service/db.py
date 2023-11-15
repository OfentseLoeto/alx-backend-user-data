#!/usr/bin/env python3
"""
Db module
"""
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """
    The database class
    """
    Session = sessionmaker()

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

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add user to the database

        Args:
          - email(str): User's email
          - hashed_password: User's hashed_password

        Return:
          - Created user object
        """

        # Create a new User instance.
        user = User(email=email, hashed_password=hashed_password)

        # Add a new user to the session.
        self._session.add(user)

        # Commit changes to the database
        self._session.commit()

        # Refresh the user instance to get the updated ID from the database
        self._session.refresh(user)

        # Return the created user object
        return user

    def find_user_by(self, **kwargs):
        """
        """
        session = self.Session()
        try:
            user = session.query(User).filter_by(**kwargs).first()

            if user is None:
                raise NoResultFound("No user found")

            return user
        except InvalidRequestError as e:
            session.rollback()
            raise e

        finally:
            session.close()
