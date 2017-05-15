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
from meerkat_nest.util import scramble, format_form_field_key
from meerkat_nest import message_service

db_url = os.environ['MEERKAT_NEST_DB_URL']
engine = create_engine(db_url)

class amendData(Resource):
    """
    Receives JSON data and amends an existing entry in Meerkat DB
    
    Returns:\n
        HTTP return code\n
    """
    #decorators = [authenticate]

    def get(self):
        return "amend data GET"

    def post(self):

        data_entry = request.json

        valid = validate_request(data_entry)
        if not valid['value']:
            return {"message":"Input was not a valid Meerkat Nest JSON object"}

        uuid_pk = upload_to_raw_data(data_entry)

        if not uuid_pk:
            return {"message":"Raw input type '" + data_entry['content'] + "' is not supported"}

        processed_data_entry = process(uuid_pk, data_entry)

        if not processed_data_entry:
            return {"message":"Data type '" + data_entry['formId'] + "' is not supported for input type '" + data_entry['content'] + "'"}

        sent = message_service.send_data(processed_data_entry)

        return processed_data_entry

def amend_raw_data(data_entry):
    """
    Stores raw data in Meerkat Nest database
    
    Returns:\n
        uuid for the PK of the raw data row\n
    """

    uuid_pk = str(uuid.uuid4())

    insert_row = None

    if data_entry['content'] == 'form':
        insert_row = model.rawDataOdkCollect.__table__.insert().values(
                uuid =uuid_pk,
                received_on = datetime.datetime.now(),
                active_from = datetime.datetime.now(),
                authentication_token = data_entry['token'],
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
            print(e)
            return False

        return uuid_pk

    else:
        return False

def validate_request(data_entry):
    """
    Validates the data entry as supported input
    
    Returns:\n
        True if processing was successful, False otherwise
    """

    try:
        assert('token' in data_entry)
        assert('content' in data_entry)
        assert(data_entry['content'] in config.country_config['supported_content'])

        assert('formId' in data_entry)
        assert('formVersion' in data_entry)
        assert('data' in data_entry)
        return {"value":1, "message":"valid"}
    except AssertionError as e:
        return {"value":0,"message":str(e)}
