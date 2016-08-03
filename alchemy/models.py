#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""SQLalchemy modles for budget app.

This is the database interation model. To interact with the database,
create a engine specific model that can use these models.
"""

import datetime
import errno
import os
from hashlib import sha1, sha256


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Sequence,
    String,
    UniqueConstraint)


__author__ = 'Brett R. Ward'


# Constants
ENCODING = 'utf-8'

# Create base for model objects to inherrit.
BASE = declarative_base()


class User(BASE):
    """A user represents a person that interfaces with the database."""

    __tablename__ = 'users'

    # Columns
    id = Column(Integer, Sequence('user_id'), primary_key=True)
    user_name = Column(String(64), unique=True)
    first_name = Column(String(64))
    middle_name = Column(String(64))
    last_name = Column(String(64))
    created = Column(DateTime)
    salt = Column(String(40))
    password = Column(String(64))

    def __init__(self, **kwds):
        """Set created time on new objects."""
        super().__init__(**kwds)
        self.created = datetime.datetime.utcnow()
        self.salt = self.create_salt()
        self.password = self.get_password(self.password)

    def __str__(self):
        """Print user pretty when called as a string."""
        return '<User(user_name={}, first_name={}, created={})>'.format(
            self.user_name,
            self.first_name,
            self.created)

    def create_salt(self):
        """Create a new salt value."""
        return sha1(
            str(datetime.datetime.utcnow()).encode(ENCODING)).hexdigest()

    def get_password(self, password):
        """Return hashed password."""
        temp = '{}{}'.format(self.salt, password)
        return sha256(temp.encode(ENCODING)).hexdigest()
