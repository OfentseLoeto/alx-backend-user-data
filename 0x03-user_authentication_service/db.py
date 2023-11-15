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

# Auth module

from typing import Optional

class Auth:
    """Auth class
    """

    def __init__(self, db: DB) -> None:
        """Initialize a new Auth instance

        Args:
            db (DB): The database instance
        """
        self._db = db

    def register_user(self, email: str, hashed_password: str) -> Optional[User]:
        """Register a new user

        Args:
            email (str): User's email
            hashed_password (str): User's hashed password

        Returns:
            Optional[User]: The created User object or None if registration fails
        """
        existing_user = self.get_user_by_email(email)
        if existing_user:
            return None  # User with this email already exists

        return self._db.add_user(email, hashed_password)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email

        Args:
            email (str): User's email

        Returns:
            Optional[User]: The User object or None if not found
        """
        session = self._db._session  # Only public methods of DB should be used
        return session.query(User).filter_by(email=email).first()


# Flask app

from flask import Flask, request, jsonify

app = Flask(__name__)
db = DB()
auth = Auth(db)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    hashed_password = data.get('hashed_password')

    if not email or not hashed_password:
        return jsonify({'error': 'Missing required fields'}), 400

    user = auth.register_user(email, hashed_password)
    if user:
        return jsonify({'message': 'Registration successful', 'user_id': user.id})
    else:
        return jsonify({'error': 'User with this email already exists'}), 400

if __name__ == '__main__':
    app.run(debug=True)


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
