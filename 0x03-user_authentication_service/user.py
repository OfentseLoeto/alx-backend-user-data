#!/usr/bin/env python3
"""
Creating a SQLAlchemy model named User for a
database table named users
-By using the mapping declaration of SQLAlchemy
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

    def __repr__(self):
        return "< User(email='%s', hashed_password='%s', session_id='%s', reset_token='%s') >" % (
                self.email, self.hashed_password, self.session_id,
                self.reset_token
                )
