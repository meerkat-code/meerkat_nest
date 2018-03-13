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


class DeactivateData(Resource):

    def post(self):
        """
        Not implemented. Receives JSON data and stores it in Meerkat Nest database

        Returns:\n
            HTTP return code\n
        """

        logging.debug("received deactivation request")
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
        # Deactivate the data entry in the raw storage
        try:
            deactivate_data_entry(data_entry)
        except Exception as e:
            msg = "Error in deactivating data: " + e.args[0]
            logging.error(msg)
            return Response(json.dumps({"message": msg}),
                            status=502,
                            mimetype='application/json')

        # Delete the data entry from the processed data
        try:
            delete_from_processed(data_entry)
        except AssertionError as e:
            msg = "Data type '" + data_entry['formId'] + "' is not supported for input type '"\
                + data_entry['content'] + "'"
            logging.error(msg)
            return Response(json.dumps({"message": msg}),
                            status=400,
                            mimetype='application/json')

        # Send deactivation message to the cloud
        try:
            data_entry_delete = message_service.send_deactivation_message(data_entry)
        except AssertionError as e:
            msg = "Error in sending deactivation message to message queue: " + str(e)
            logging.error(msg)
            return Response(json.dumps({"message": msg}),
                            status=502,
                            mimetype='application/json')

        logging.debug("processed deactivation request")
        return Response(json.dumps(data_entry_delete),
                        status=200,
                        mimetype='application/json')


def deactivate_data_entry(data_entry):

    deactivate_row = model.RawDataOdkCollect.__table__.insert().values(
            active_until=datetime.datetime.now()
    ).where(
        model.RawDataOdkCollect.uuid == data_entry['uuid']
    )

    try:
        connection = engine.connect()
        connection.execute(deactivate_row)
        connection.close()
        return data_entry
    except Exception as e:
        raise


def delete_from_processed(data_entry):
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    delete_row_query = session.query(model.data_type_tables[data_entry['formId']])\
        .filter(model.data_type_tables[data_entry['formId']].uuid == data_entry['uuid']).all()

    assert len(delete_row_query) > 0, "No record with uuid " + data_entry['uuid'] + " found"
    assert len(delete_row_query) < 2, "Multiple records with uuid " + data_entry['uuid'] + " found"

    delete_row = delete_row_query[0]

    try:
        session.delete(delete_row)
        session.commit()
        session.flush()
    except Exception as e:
        raise



