#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""SQLalchemy models for budget application.

This is the database interaction model. To interact with the database,
create an engine to specify the database that can use these models.
"""

import datetime
from hashlib import sha1, sha256


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Sequence,
    String)


__author__ = 'Brett R. Ward'


# Constants
ENCODING = 'utf-8'

# Create base for model objects to inherit.
BASE = declarative_base()


class User(BASE):
    """A user represents a person that interfaces with the database."""

    __tablename__ = 'users'

    # Columns
    id = Column(Integer, Sequence('user_id'), primary_key=True)
    user_name = Column(String(64), unique=True, nullable=False)
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

    @staticmethod
    def create_salt():
        """Create a new salt value."""
        return sha1(
            str(datetime.datetime.utcnow()).encode(ENCODING)).hexdigest()

    def get_password(self, password):
        """Return hashed password."""
        temp = '{}{}'.format(self.salt, password)
        return sha256(temp.encode(ENCODING)).hexdigest()


class BudgetGroup(BASE):
    """A budget group is a collection of budgets.

    Used for reporting by category.
    """

    __tablename__ = 'budget_groups'

    # Columns
    id = Column(Integer, Sequence('budget_groups_id'), primary_key=True)
    name = Column(String(64), nullable=False)

    # Relationships
    budgets = relationship(
        'Budget', order_by='asc(Budget.id)', backref='budget_group')


class Budget(BASE):
    """Itemization's are categorized in budgets."""

    __tablename__ = 'budgets'

    # Columns
    id = Column(Integer, Sequence('budget_id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('budget_groups.id'))
    name = Column(String(64), nullable=False)

    # Relationships
    items = relationship('Item', order_by='asc(Item.id)', backref='budget')


class Transaction(BASE):
    """A transaction that can be related to a physical receipt or bank account.

    Each transaction will contain at least one itemization that will tie it to
    a budget.
    """

    __tablename__ = 'transactions'

    # Columns
    id = Column(Integer, Sequence('transaction_id'), primary_key=True)
    name = Column(String(64), nullable=False)
    date = Column(DateTime)

    # Relationships
    items = relationship('Item', order_by='asc(Item.id)', backref='transaction')


class Item(BASE):
    """Item is an itemization of a transaction tied to a Budget."""

    __tablename__ = 'itemizations'

    # Columns
    id = Column(Integer, Sequence('item_id'), primary_key=True)
    budget_id = Column(Integer, ForeignKey('budgets.id'))
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    name = Column(String(64), nullable=False)
    amount_in_cents = Column(Integer)
