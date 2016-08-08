#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Add some usrers to the budget app.

This will require us to import the table class from models.
"""


import json


# import 3rd party


from models import User
from sqlite_engine import session_scope


__author__ = 'Brett R. Ward'

# Constants
USER_LIST = 'users.json'


def main():
    """Insert some Users into the database."""
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
