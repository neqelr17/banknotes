#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Create budget tables.

Used to create tables.
"""

from sqlalchemy import create_engine

from models import BASE

__author__ = 'Brett R. Ward'

# Constants


def main():
    """Main call.

    Runs main app that creates tables for the Imported Base if the do not exist
    """
    # Create engine and create tables that do not exists
    # engine = create_engine('postgresql+pg8000://{0}:{1}@{2}/{3}'.format(
    # engine = create_engine('postgresql+psycopg2://{0}:{1}@{2}/{3}'.format(
    #     PG_UNAME, PG_PASS, PG_HOST, PG_DB))
    engine = create_engine('sqlite:///budget.db')
    print('Creating Tables')
    BASE.metadata.create_all(engine, checkfirst=True)
    print('Success!')

# end main()

# main call
if __name__ == "__main__":
    main()
