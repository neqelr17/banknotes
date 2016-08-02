#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""SQLalchemy modles for budget app.

models for pivot audit db. This is designed to only import from
there is no driver code here.
"""

from hashlib import sha1
from enum import Enum


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import (Column,
                        Date,
                        DateTime,
                        ForeignKey,
                        Integer,
                        Sequence,
                        String,
                        UniqueConstraint)


__author__ = 'Brett R. Ward'


BASE = declarative_base()


class User(BASE):
    """A user represents a person that interfaces with the database."""

    __tablename__ = 'users'

    # Columns
    id = Column(Integer, Sequence('user_id'), primary_key=True)
    first_name = Column(String(64))
    middle_name = Column(String(64))
    last_name = Column(String(64))
    alias = Column(String(64))
    created = Column(DateTime)
    salt = Column(String(40))
    password = Column(String(64))
