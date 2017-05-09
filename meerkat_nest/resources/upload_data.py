"""
Data resource for upload data
"""
from flask_restful import Resource
from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import os
import uuid
import datetime
from pprint import pprint

from meerkat_nest import model
from meerkat_nest import config

db_url = os.environ['MEERKAT_NEST_DB_URL']
engine = create_engine(db_url)

class uploadData(Resource):
    """
    Receives JSON data and stores it in Meerkat Nest database
    
    Returns:\n
        HTTP return code\n
    """
    #decorators = [authenticate]

    def get(self):
        return "upload data GET"

    def post(self):

        data_entry = request.json


        # Validate request
        try:
            assert('token' in data_entry)
            assert('content' in data_entry)
            assert('formId' in data_entry)
            assert('formVersion' in data_entry)
            assert('data' in data_entry)
        except AssertionError:
            return {"message":"Input was not a valid Meerkat Nest JSON item"}

        uuid_pk = upload_to_raw_data(data_entry = data_entry)

        if not uuid_pk:
            return {"message":"Raw input type '" + data_entry['content'] + "' is not supported"}

        entered = process(uuid_pk, data_entry)

        if not entered:
            return {"message":"Data type '" + data_entry['formId'] + "' is not supported for input type '" + data_entry['content'] + "'"}

        return data_entry

def upload_to_raw_data(data_entry):
    """
    Stores data in Meerkat Nest database
    
    Returns:\n
        uuid for the PK of the raw data row\n
    """

    uuid_pk = str(uuid.uuid4())

    insert_row = None
    if data_entry['content'] == 'form':
        insert_row = model.rawDataOdkCollect.__table__.insert().values(
                uuid =uuid_pk,
                timestamp = datetime.datetime.now(),
                token = data_entry['token'],
                content = data_entry['content'],
                formId = data_entry['formId'],
                formVersion = data_entry['formVersion'],
                data = data_entry['data']
            )

    if insert_row is not None:
        try:
            connection = engine.connect()
            connection.execute(insert_row)
            connection.close()
        except Exception as e:
            return None

        return uuid_pk

    else:
        return False

def process(uuid_pk, data_entry):

    insert_row = None
    if data_entry['content'] == 'form':
        if data_entry['formId'] in config.country_config['tables']:
            insert_row = model.data_type_tables[data_entry['formId']].__table__.insert().values(
                   uuid=uuid_pk,
                   data=data_entry['data']
                )
    if insert_row is not None:
        try:
            connection = engine.connect()
            connection.execute(insert_row)
            connection.close()
            return True
        except Exception as e:
            return False
        

    else:
        return False