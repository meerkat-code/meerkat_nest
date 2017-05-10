"""
Data resource for downloading data
"""
from flask_restful import Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import os
from pprint import pprint

from meerkat_nest import model

from meerkat_nest import config

db_url = os.environ['MEERKAT_NEST_DB_URL']
engine = create_engine(db_url)

#TODO: replace with actual country configs

class downloadData(Resource):
    def get(self):
        """
        Initiates the download of the whole data set from Meerkat Nest
        
        Returns:\n
            HTTP return code\n
        """
        Session = sessionmaker(bind=engine)
        session = Session()

        ret = {}

        for table in config.country_config['tables']:
            ret[table] = str(session.query(model.data_type_tables[table].data).all())


        return ret

