"""
Meerkat Nest Test

Unit tests Meerkat Nest
"""

import requests
import meerkat_nest
from meerkat_nest.test import test_data
from meerkat_nest import config
from meerkat_nest.test.test_data.upload_payload import upload_payload

from unittest import mock
import unittest


class MeerkatNestTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # test upload data flow
    # validate_request, upload_to_raw_data, process,  message_service.send_data
    @mock.patch('meerkat_nest.resources.upload_data.validate_request')
    @mock.patch('meerkat_nest.resources.upload_data.upload_to_raw_data')
    @mock.patch('meerkat_nest.message_service.send_data')
    def test_valid_upload(self, request_mock):
    	
        self.app.post('/upload', data=upload_payload)

    # test authentication

    # test validating data
    def test_data_validation(self, request_mock):
        pass

    # test processing data
    def test_data_processing(self, request_mock):
        pass

    # test sending data to SQS
    @mock.patch('meerkat_nest.message_service.sqs_client.send_message')
    @mock.patch('meerkat_nest.message_service.sns_client.publish')
    def test_data_sending(self, request_mock):
        pass

    #@mock.patch('meerkat_nest.task_queue.requests')


