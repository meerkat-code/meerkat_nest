"""
Data resource for upload data
"""
import re
from flask_restful import Resource
from flask import request, Response
from sqlalchemy import create_engine
import json
import os
import uuid
import datetime
import logging
import copy

from meerkat_nest import model
from meerkat_nest import config
from meerkat_nest.util import scramble, validate_request, hash
from meerkat_nest import message_service
from meerkat_nest.util import translate_patient_id

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

        logging.error("Validating request: " + str(datetime.datetime.now()))
        # Validate the request
        try:
            validate_request(data_entry)
        except AssertionError as e:
            msg = "Input was not a valid Meerkat Nest JSON object: " + e.args[0]
            logging.error(msg)
            return Response(json.dumps({"message": msg}),
                            status=400,
                            mimetype='application/json')

        logging.error("Uploading raw data: " + str(datetime.datetime.now()))
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
            logging.error(msg, exc_info=True)
            return Response(json.dumps({"message": msg}),
                            status=502,
                            mimetype='application/json')

        logging.error("Processing data: " + str(datetime.datetime.now()))
        # Process the data entry
        try:
            processed_data_entry = process(data_entry)
        except AssertionError as e:
            msg = "Data type '" + data_entry['formId'] + "' is not supported for input type '" \
                  + data_entry['content'] + "'"
            logging.error(msg)
            return Response(json.dumps({"message": msg}),
                            status=400,
                            mimetype='application/json')

        logging.error("Storing processed data: " + str(datetime.datetime.now()))
        # Store processed data entry in Nest
        try:
            store_processed_data(processed_data_entry)
        except Exception as e:
            msg = "Error in uploading data: " + e.args[0]
            logging.error(msg, exc_info=True)
            return Response(json.dumps({"message": msg}),
                            status=502,
                            mimetype='application/json')

        logging.error("Sending to cloud: " + str(datetime.datetime.now()))
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

        logging.error("Done: " + str(datetime.datetime.now()))
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


def store_processed_data(data_entry):
    insert_row = model.data_type_tables[data_entry['formId']].__table__.insert().values(
        uuid=data_entry['uuid'],
        data=data_entry['data']
    )

    try:
        connection = engine.connect()
        connection.execute(insert_row)
        connection.close()
        return data_entry
    except Exception:
        raise


def process(data_entry):
    """
    Processes raw data and stores the processed data entry in in Meerkat Nest database
    
    Returns:\n
        processed data_entry if processing was successful, False otherwise
    """

    assert data_entry['content'] in ['form', 'record'], "Content not supported"
    assert data_entry['formId'] in config.country_config['tables'], "Form not supported"

    processed_data_entry = restructure_aggregate_data(data_entry)
    processed_data_entry = process_patient_id(processed_data_entry)
    processed_data_entry = scramble_fields(processed_data_entry)
    processed_data_entry = hash_fields(processed_data_entry)
    processed_data_entry = format_field_keys(processed_data_entry)
    processed_data_entry = format_form_name(processed_data_entry)

    return processed_data_entry


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


def process_patient_id(data_entry):
    patient_id_configs_ = config.country_config.get('patient_id')
    patient_id_config = patient_id_configs_.get(data_entry['formId'])
    if not patient_id_config:
        return data_entry

    field_name_ = patient_id_config['field_name']
    new_patient_id = data_entry.get(field_name_)
    if not new_patient_id:
        return data_entry

    if patient_id_config['translate']:
        new_patient_id = translate_patient_id.translate(new_patient_id)

    validation_regexp_str = patient_id_config['validate']
    excluded_ids = patient_id_config['exclude']
    if validation_regexp_str or new_patient_id in excluded_ids:
        validation = re.compile(validation_regexp_str)
        if not validation.match(new_patient_id):
            data_entry[field_name_] = None
            return data_entry

    data_entry[field_name_] = new_patient_id
    return data_entry


def scramble_fields(data_entry):
    """
    Scrambles fields in data entry based on configurations
    
    Returns:\n
        data entry structure with scrambled fields
    """

    data_entry_scrambled = data_entry

    fields = config.country_config.get('scramble_fields', {}).get(data_entry['formId'], {})

    for field in fields:
        if field in data_entry_scrambled['data'].keys():
            data_entry_scrambled['data'][field] = scramble(data_entry_scrambled['data'][field])

    return data_entry_scrambled


def hash_fields(data_entry):
    """
    Hashes fields in data entry based on configurations

    Returns:\n
        data entry structure with encrypted fields
    """

    data_entry_hashed = data_entry

    fields = config.country_config.get('hash_fields', {}).get(data_entry['formId'], {})

    for field in fields:
        if field in data_entry_hashed['data'].keys():
            data_entry_hashed['data'][field] = hash(data_entry_hashed['data'][field])

    return data_entry_hashed


def format_field_keys(data_entry):
    """
    Formats the field names in the data entry
    
    Returns:\n
        data entry structure with formatted field namess
    """

    rename_fields = config.country_config.get('rename_fields',
                                              {}).get(data_entry['formId'], {})
    character_replacements = config.country_config.get('replace_characters', 
                                                       {}).get(data_entry['formId'], [])
    data_fields = data_entry['data'].keys()

    # Perform character replacements to all fields
    for characters in character_replacements:
        for key in data_fields:
            if characters[0] in key:
                data_entry['data'][key.replace(characters[0],characters[1])] = data_entry['data'][key]
                data_entry['data'].pop(key)

    # Perform key replacements
    for key in rename_fields:
        if key in data_fields:
            data_entry['data'][rename_fields[key]] = data_entry['data'][key]
            data_entry['data'].pop(key)

    return data_entry


def format_form_name(data_entry):
    """
    Formats the form name of the data entry

    Returns:\n
        data entry structure with formatted form name
    """

    rename_form = config.country_config.get('rename_forms',
                                              {}).get(data_entry['formId'], None)

    if rename_form:
        data_entry['formId'] = rename_form

    return data_entry
