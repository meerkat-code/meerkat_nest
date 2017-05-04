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

        pprint("DEBUG: Received POST request")
        pprint(request.json)
        data_entry = request.json

        # Validate request
        try:
            assert('token' in data_entry)
            assert('content' in data_entry)
            assert('formId' in data_entry)
            assert('formVersion' in data_entry)
            assert('data' in data_entry)
        except AssertionError:
            return {"message":"Input was not valid ODK Aggregate JSON item"}

        upload_to_raw_data(content=data_entry['content'], data_entry=data_entry)

        return data_entry

def upload_to_raw_data(content, data_entry):

    Session = sessionmaker(bind=engine)
    session = Session()

    if content == 'test':
        model.rawDataOdkCollect.__table__.insert(
                uuid = str(uuid.uuid4()),
                timestamp = datetime.datetime.now(),
                token = data_entry['token'],
                content = data_entry['content'],
                formId = data_entry['content'],
                formVersion = data_entry['content'],
                data = data_entry['content']
            )
