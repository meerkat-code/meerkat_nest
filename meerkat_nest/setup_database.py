from sqlalchemy import create_engine, exc
from sqlalchemy_utils import database_exists, create_database, drop_database
import time
import logging

from meerkat_nest import model


def create_db(url, base, drop=False):
    """
    The function creates the database

    Args:
        url : the database_url
        base: An SQLAlchmey declarative base with the db schema
        drop: Flag to drop the database before creating it

    Returns:
        Boolean: True
    """
    counter = 0
    while counter < 5:
        try:
            if drop and database_exists(url):
                print('Dropping database.')
                drop_database(url)
            if not database_exists(url):
                print('Creating database.')
                create_database(url)
                break

        except exc.OperationalError as e:
            logging.error('There was an error connecting to the db.')
            logging.error(e)
            logging.error('Trying again in 5 seconds...')
            time.sleep(5)
        
        counter = counter + 1

    engine = create_engine(url)
    connection = engine.connect()
    connection.close()
    model.Base.metadata.create_all(engine)
    return True
