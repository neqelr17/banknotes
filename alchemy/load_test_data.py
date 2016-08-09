#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Add some usrers to the budget app.

This will require us to import the table class from models.
"""


import json
from datetime import datetime


# import 3rd party


from models import User, BudgetGroup, Budget, Transaction, Item
from sqlite_engine import session_scope


__author__ = 'Brett R. Ward'

# Constants
USER_LIST = 'test_data.json'


def main():
    """Insert some Users into the database."""
    with open(USER_LIST, 'r') as fh_users:
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


if __name__ == "__main__":
    main()
