"""
Data resource for upload data
"""
from flask_restful import Resource
from flask import request, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import os
import uuid
import datetime
import logging
from pprint import pprint

from meerkat_nest import model
from meerkat_nest import config
from meerkat_nest.util import scramble, format_form_field_key, validate_request
from meerkat_nest import message_service

db_url = os.environ['MEERKAT_NEST_DB_URL']
engine = create_engine(db_url)


class UploadData(Resource):
    """
    Receives JSON data and stores it in Meerkat Nest database
    
    Returns:\n
        HTTP return code\n
    """

    def get(self):
        return "upload data GET"

    def post(self):

        logging.debug("received upload request")
        logging.debug(str(request.headers))
        data_entry = request.get_json()
        logging.debug(str(data_entry))

        # Validate the request
        try:
            validate_request(data_entry)
        except AssertionError as e:
            msg = "Input was not a valid Meerkat Nest JSON object: " + e.args[0]
            logging.error(msg)
            return Response(json.dumps({"message": msg}),
                            status=400,
                            mimetype='application/json')
        # Upload the data entry in to raw data storage
        try:
            uuid_pk = upload_to_raw_data(data_entry)
            # data_entry['uuid'] = uuid_pk
        except AssertionError as e:
            msg = "Raw input type '" + data_entry['content'] + "' is not supported"
            logging.error(msg)
            return Response(json.dumps({"message": msg}),
                            status=400,
                            mimetype='application/json')
        except Exception as e:
            msg = "Error in uploading data: " + e.args[0]
            logging.error(msg)
            return Response(json.dumps({"message": msg}),
                            status=502,
                            mimetype='application/json')

        # Process the data entry
        try:
            processed_data_entry = process(data_entry)
        except AssertionError as e:
            msg = "Data type '" + data_entry['formId'] + "' is not supported for input type '"\
                + data_entry['content'] + "'"
            logging.error(msg)
            return Response(json.dumps({"message": msg}),
                            status=400,
                            mimetype='application/json')

        # Send processed data forward to the cloud
        try:
            sent = message_service.send_data(processed_data_entry)
        except AssertionError as e:
            msg = "Error in forwarding data to message queue: " + str(e)
            logging.error(msg)
            return Response(json.dumps({"message": msg}),
                            status=502,
                            mimetype='application/json')

        logging.debug("processed upload request")
        return Response(json.dumps(processed_data_entry),
                        status=200,
                        mimetype='application/json')


def upload_to_raw_data(data_entry):
    """
    Stores raw data in Meerkat Nest database
    
    Returns:\n
        uuid for the PK of the raw data row\n
    """

    uuid_pk = str(uuid.uuid4())

    insert_row = None

    if data_entry['content'] == 'record':
        insert_row = model.RawDataOdkCollect.__table__.insert().values(
                uuid=uuid_pk,
                received_on=datetime.datetime.now(),
                active_from=datetime.datetime.now(),
                authentication_token=data_entry['token'],
                content=data_entry['content'],
                formId=data_entry['formId'],
                formVersion=data_entry['formVersion'],
                data=data_entry['data']
        )

    assert insert_row is not None, "Content handling not implemented"

    connection = engine.connect()
    connection.execute(insert_row)
    connection.close()

    return uuid_pk


def process(data_entry):
    """
    Processes raw data and stores the processed data entry in in Meerkat Nest database
    
    Returns:\n
        processed data_entry if processing was successful, False otherwise
    """
    processed_data_entry = restructure_aggregate_data(data_entry)
    processed_data_entry = scramble_fields(processed_data_entry)
    processed_data_entry = format_field_keys(processed_data_entry)

    assert data_entry['content'] in ['form', 'record'], "Content not supported"
    assert data_entry['formId'] in config.country_config['tables'], "Form not supported"

    insert_row = model.data_type_tables[processed_data_entry['formId']].__table__.insert().values(
           uuid=processed_data_entry['uuid'],
           data=processed_data_entry['data']
        )

    try:
        connection = engine.connect()
        connection.execute(insert_row)
        connection.close()
        return processed_data_entry
    except Exception as e:
        raise


def restructure_aggregate_data(data_entry):
    """
    Restructures data from aggregate JSON feed
    
    Returns:\n
        restructured data entry
    """

    restructured_data = data_entry['data'][0]
    data_entry['data'] = restructured_data

    data_entry['uuid'] = data_entry['data']['*meta-instance-id*']

    return data_entry


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
            data_entry_scrambled['data'][field] = scramble(data_entry_scrambled['data'][field])

    return data_entry_scrambled


def format_field_keys(data_entry):
    """
    Formats the field names in the data entry
    
    Returns:\n
        data entry structure with formatted field namess
    """

    new_data_entry = data_entry
    new_data_entry['data'] = {}

    for key in data_entry['data'].keys():
        new_key = format_form_field_key(key)
        new_data_entry['data'].update({new_key: data_entry['data'][key]})

    return data_entry 
