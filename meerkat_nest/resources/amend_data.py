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

        try:
            validate_request(data_entry)
        except AssertionError as e:
            return {"message":"Input was not a valid Meerkat Nest JSON object: " + e.args[0]}

        try:
            uuid_pk = amend_raw_data(data_entry)
        except AssertionError as e:
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

    assert(data_entry['content'] in ['form'])

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
            raise

        return uuid_pk

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
        assert('uuid' in data_entry['data'])
        return {"value":1, "message":"valid"}
    except AssertionError as e:
        message = e.args[0]
        message += "\nRequest validation failed."
        e.args = (message,) #wrap it up in new tuple
        raise

    """try:
        Session = sessionmaker(bind=engine)
        session = Session()
        validation_select = session.query(model.rawDataOdkCollect.uuid).filter(model.rawDataOdkCollect.uuid = data_entry['data']['uuid']).all()
    except Exception as e:
        print(e)
        raise"""
