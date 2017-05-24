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

        try:
            validate_request(data_entry)
        except AssertionError as e:
            return {"message":("Input was not a valid Meerkat Nest JSON object: " + e.args[0])}

        try:
            uuid_pk = upload_to_raw_data(data_entry)
        except AssertionError as e:
            return {"message":"Raw input type '" + data_entry['content'] + "' is not supported"}
        except Exception as e:
            return {"message": "Error in uploading data: " + e.args[0]}

        try:
            processed_data_entry = process(uuid_pk, data_entry)
        except AssertionError as e:
            return {"message":"Data type '" + data_entry['formId'] + "' is not supported for input type '" + data_entry['content'] + "'"}

        try:
            sent = message_service.send_data(processed_data_entry)
        except AssertionError as e:
            return {"message":"Error in forwarding data to message queue: " + str(e)}#e.args[0]}

        return processed_data_entry

def upload_to_raw_data(data_entry):
    """
    Stores raw data in Meerkat Nest database
    
    Returns:\n
        uuid for the PK of the raw data row\n
    """

    uuid_pk = str(uuid.uuid4())

    insert_row = None

    assert data_entry['content'] in ['form'], "Content not supported"

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

    assert insert_row is not None, "Content handling not implemented"
    try:
        connection = engine.connect()
        connection.execute(insert_row)
        connection.close()
    except Exception as e:
        raise

    return uuid_pk

def process(uuid_pk, data_entry):
    """
    Processes raw data and stores the processed data entry in in Meerkat Nest database
    
    Returns:\n
        processed data_entry if processing was successful, False otherwise
    """

    processed_data_entry = scramble_fields(data_entry)
    processed_data_entry = format_field_keys(processed_data_entry)

    return processed_data_entry

    assert data_entry['content'] in ['form'], "Content not supported"
    assert data_entry['formId'] in config.country_config['tables'], "Form not supported"

    insert_row = model.data_type_tables[processed_data_entry['formId']].__table__.insert().values(
           uuid=uuid_pk,
           data=processed_data_entry['data']
        )

    try:
        connection = engine.connect()
        connection.execute(insert_row)
        connection.close()
        return processed_data_entry
    except Exception as e:
        raise

    return processed_data_entry

def scramble_fields(data_entry):
    """
    Scrambles fields in data entry based on configurations
    
    Returns:\n
        data entry structure with scrambled fields
    """

    data_entry_scrambled = data_entry

    try:
        fields = config.country_config['scramble_fields'][data_entry['formId']]
    except KeyError as e:
        return data_entry_scrambled

    for field in fields:
        if field in data_entry_scrambled['data'].keys():
            data_entry_scrambled['data'][field]=scramble(data_entry_scrambled['data'][field])

    return data_entry_scrambled

def format_field_keys(data_entry):
    """
    Formats the field names in the data entry
    
    Returns:\n
        data entry structure with formatted field namess
    """

    for key in data_entry['data'].keys():
        new_key = format_form_field_key(key)
        if new_key != key:
            data_entry['data'].update({new_key: data_entry['data'][key]})
            data_entry['data'].pop(key)

    return data_entry 

def validate_request(data_entry):
    """
    Validates the data entry as supported input
    
    Returns:\n
        True if processing was successful, False otherwise
    """
    valid_data_structure = {
        'key_token': 'token',
        'key_content': 'content',
        'key_formId': 'formId',
        'key_formVersion': 'formVersion',
        'key_data': 'data'
    }

    try:
        for key in valid_data_structure:
            assert valid_data_structure[key] in data_entry, "Missing key '" + valid_data_structure[key] + "' in input data"
            assert data_entry['content'] in config.country_config['supported_content'], "Content '" + data_entry['content'] + "'' not supported"
    except AssertionError as e:
        message = e.args[0]
        message += "\nRequest validation failed."
        e.args = (message,)
        raise
