#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Remove and create a dev database.

Contains dev engine.
Main will remove test db and create new one with any updates in models.py
"""

import errno
import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models import BASE, User, BudgetGroup, Budget, Transaction, Item


__author__ = 'Brett R. Ward'

# Constants
DB_NAME = 'budget.db'
TEST_DATA = 'test_data.json'

# Create ENGINE
ENGINE = create_engine('sqlite:///{}'.format(DB_NAME))

# Create SESSION
SESSION = sessionmaker(bind=ENGINE)


def main():
    """Delete test sqlite db and create new one with.

    This is only for dev! This just makes it easy to remove
    and create a new test db.
    """
    # Remove old db
    remove_test_db(DB_NAME)

    print('Creating Tables')
    BASE.metadata.create_all(ENGINE, checkfirst=True)
    print('Success!')

    # Open up test data json and load data to database.
    if len(sys.argv) < 2:
        with open(TEST_DATA, 'r') as fh_users:
            data = json.load(fh_users)
        with session_scope() as session:
            add_users(data, session)
            add_budgets(data, session)


def add_budgets(data, session):
    """Add budgets from json file.

    Used for development to import test data to database.
    """
    # Groups
    food_group = BudgetGroup(name=data['groups'][0]['name'])
    auto_group = BudgetGroup(name=data['groups'][1]['name'])

    # Budgets
    fast_food = Budget(name=data['budgets'][0]['name'])
    fast_food.budget_group = food_group
    groceries = Budget(name=data['budgets'][1]['name'])
    groceries.budget_group = food_group
    gas = Budget(name=data['budgets'][2]['name'])
    gas.budget_group = auto_group

    # Transactions
    macys = Transaction(name=data['transactions'][0]['name'])
    macys.date = datetime.utcnow()
    maverick = Transaction(name=data['transactions'][1]['name'])
    maverick.date = datetime.utcnow()

    # Items
    macy_gro = Item(
        name=data['items'][0]['name'],
        amount_in_cents=data['items'][0]['amount'])
    macy_gro.budget = groceries
    macy_gro.transaction = macys
    maverrick_food = Item(
        name=data['items'][1]['name'],
        amount_in_cents=data['items'][1]['amount'])
    maverrick_food.budget = fast_food
    maverrick_food.transaction = maverick
    maverrick_gas = Item(
        name=data['items'][2]['name'],
        amount_in_cents=data['items'][2]['amount'])
    maverrick_gas.budget = gas
    maverrick_gas.transaction = maverick

    session.add(macy_gro)
    session.add(maverrick_food)
    session.add(maverrick_gas)


def add_users(data, session):
    """Add users from json file.

    Used for development to import test data to database.
    """
    for user in data['users']:
        session.add(User(
            user_name=user['user_name'],
            first_name=user['first_name'],
            middle_name=user['middle_name'],
            last_name=user['last_name'],
            password=user['password']
        ))


def remove_test_db(filename):
    """Quietly removes the database file if it exists."""
    try:
        os.remove(filename)
    except OSError as exc:
        if exc.errno != errno.ENOENT:
            raise
    else:
        print('Old database file removed.')


@contextmanager
def session_scope():
    """Provide a transactional scope for a series of database interactions.

    Used to automatically handle the commiting and rollback on errors.
    """
    session = SESSION()
    try:
        yield session
        session.commit()
    except Exception as exc:
        print(exc)
        session.rollback()
        raise exc
    finally:
        session.close()


if __name__ == "__main__":
    main()
