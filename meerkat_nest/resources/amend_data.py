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
from meerkat_nest.util import scramble, format_form_field_key, validate_request, raw_odk_data_to_dict
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
            new_row = amend_raw_data(data_entry)
        except AssertionError as e:
            return {"message":"No record with uuid " + data_entry['uuid'] + " found"}

        return raw_odk_data_to_dict(new_row)

        processed_data_entry = process(uuid_pk, data_entry)

        if not processed_data_entry:
            return {"message":"Data type '" + data_entry['formId'] + "' is not supported for input type '" + data_entry['content'] + "'"}

        sent = message_service.send_data(processed_data_entry)

        return processed_data_entry

def amend_raw_data(data_entry):
    """
    Amends raw data in Meerkat Nest database
    
    Returns:\n
        uuid for the PK of the raw data row\n
    """

    assert(data_entry['content'] in ['form'])

    if data_entry['content'] == 'form':
        Session = sessionmaker(bind=engine)
        session = Session()
        old_row_query = session.query(model.rawDataOdkCollect)\
            .filter(model.rawDataOdkCollect.uuid == data_entry['uuid']).all()

        assert len(old_row_query) == 1, "No record with uuid " + data_entry['uuid'] + " found"

        old_row = old_row_query[0]

        new_uuid = str(uuid.uuid4())

        timestamp_now = datetime.datetime.now()

        archived_row = model.rawDataOdkCollectArchive(
            uuid = data_entry['uuid'],
            active_uuid = new_uuid,
            received_on = old_row.received_on,
            active_from = old_row.active_from,
            active_until = timestamp_now,
            authentication_token = old_row.authentication_token,
            content = old_row.content,
            formId = old_row.formId,
            formVersion = old_row.formVersion,
            data = old_row.data
        )

        new_row = model.rawDataOdkCollect(
            uuid = new_uuid,
            received_on = old_row.received_on,
            active_from = timestamp_now,
            authentication_token = data_entry['token'],
            content = data_entry['content'],
            formId = data_entry['formId'],
            formVersion = data_entry['formVersion'],
            data = data_entry['data']
        )

        try:
            session.add(archived_row)
            session.delete(old_row)
            session.add(new_row)
            session.commit()
            session.flush()
        except Exception as e:
            raise

        return new_row

