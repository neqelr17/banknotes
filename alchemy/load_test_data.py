#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Add some usrers to the budget app.

This will require us to import the table class from models.
"""


import json


# import 3rd party


from models import User, BudgetGroup, Budget, Transaction, Item
from sqlite_engine import session_scope


__author__ = 'Brett R. Ward'

# Constants
USER_LIST = 'users.json'


def main():
    """Insert some Users into the database."""
    add_users()

    with session_scope() as session:
        # Groups
        food_group = BudgetGroup(name='Food')
        auto_group = BudgetGroup(name='Auto')

        # Budgets
        fast_food = Budget(name='Fast Food')
        fast_food.budget_group = food_group
        groceries = Budget(name='Groceries')
        groceries.budget_group = food_group
        gas = Budget(name='Gas')
        gas.budget_group = auto_group

        # Transactions
        macys = Transaction(name='Macys')
        maverick = Transaction(name='Maverick')

        # Items
        macy_gro = Item(name='Macys', amount_in_cents=12500)
        macy_gro.budget = groceries
        macy_gro.transaction = macys
        maverrick_food = Item(name='Maverrick', amount_in_cents=1299)
        maverrick_food.budget = fast_food
        maverrick_food.Transaction = maverick
        maverrick_gas = Item(name='Maverrick', amount_in_cents=3999)
        maverrick_gas.budget = gas
        maverrick_gas.Transaction = maverick

        session.add(macy_gro)
        session.add(maverrick_food)
        session.add(maverrick_gas)


def add_users():
    """Add users from json file.

    Used for development to import test data to database.
    """
    with open(USER_LIST, 'r') as fh_users:
        user_list = json.load(fh_users)

    with session_scope() as session:
        for user in user_list:
            session.add(User(
                user_name=user['user_name'],
                first_name=user['first_name'],
                middle_name=user['middle_name'],
                last_name=user['last_name'],
                password=user['password']
            ))


if __name__ == "__main__":
    main()
