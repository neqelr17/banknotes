#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Remove and create a dev database.

Contains dev engine.
Main will remove test db and create new one with any updates in models.py
"""

import errno
import os
from contextlib import contextmanager


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models import BASE


__author__ = 'Brett R. Ward'

# Constants
DB_NAME = 'budget.db'

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
