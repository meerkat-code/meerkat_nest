"""
Data resource for upload data
"""
from flask_restful import Resource
import json
from pprint import pprint

class sendData(Resource):
    """
    Receives JSON data and stores it in Meerkat Nest database
    
    Returns:\n
        HTTP return code\n
    """
    #decorators = [authenticate]

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
            return {"message":"Input was not valid ODK Aggregate JSON item"}


        pprint(data_entry)

class downloadData(Resource):
    def get(self):
        """
        Initiates the download of the whole data set from Meerkat Nest
        
        Returns:\n
            HTTP return code\n
        """
        pprint("Download data called")
