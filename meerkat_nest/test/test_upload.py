import meerkat_nest
import copy
import meerkat_nest.util
from meerkat_nest import app
from meerkat_nest.test.test_data.upload_payload import upload_payload, processed_upload_payload
from meerkat_nest import message_service
from unittest import mock
import unittest
import logging
import json


class MeerkatNestUploadTest(unittest.TestCase):
    """
    Test Case class that tests uploading data into Nest
    """

    @classmethod
    def setup_class(cls):
        app.config.from_object('config.Testing')

        # Only show warning level + logs from boto3, botocore and nose.
        # Too verbose otherwise.
        logging.getLogger('boto3').setLevel(logging.WARNING)
        logging.getLogger('botocore').setLevel(logging.WARNING)
        logging.getLogger('nose').setLevel(logging.WARNING)

    def setUp(self):
        self.queue_name = 'nest-queue-demo'
        self.dead_letter_queue_name = 'nest-dead-letter-queue-demo-record'
        self.topic = 'nest-incoming-topic-demo'
        self.topic_arn = 'aws123:nest-incoming-topic-demo'
        self.data_entry = upload_payload
        self.processed_data_entry = processed_upload_payload

    def tearDown(self):
        pass

    # test upload data flow
    @mock.patch('meerkat_nest.resources.upload_data.validate_request')
    @mock.patch('meerkat_nest.resources.upload_data.upload_to_raw_data')
    @mock.patch('meerkat_nest.message_service.send_data')
    def test_valid_upload(self, mock_send_data, mock_upload_to_raw_data, mock_validate_request):
        pass

    # test validating data
    def test_data_validation(self):
        """
        Test the validation of incoming data.
        """

        # Check that a valid entry goes through
        meerkat_nest.util.validate_request(self.data_entry)

        # Check that content checking works
        with self.assertRaises(AssertionError) as e:
            faulty_data_entry = copy.deepcopy(self.data_entry)
            faulty_data_entry.pop('content')
            meerkat_nest.util.validate_request(faulty_data_entry)

        lacking_content_exception = e.exception
        self.assertEqual(str(lacking_content_exception), 'Content not defined\nRequest validation failed.')

        with self.assertRaises(AssertionError) as e:
            faulty_data_entry = copy.deepcopy(self.data_entry)
            faulty_data_entry['content'] = 'invalid-content'
            meerkat_nest.util.validate_request(faulty_data_entry)

        invalid_content_exception = e.exception
        self.assertEqual(str(invalid_content_exception),
                         'Content \'invalid-content\' not supported\nRequest validation failed.')

        # TODO: Test structure validation

    # test processing data
    def test_data_processing(self):
        """
        Test data processing.
        """
        # TODO: Test scrambling
        meerkat_nest.resources.upload_data.process(self.data_entry)

        # TODO: Test column name conversion
        pass

    # Test sending data to Meerkat Drill
    def test_data_sending(self):
        """
        TODO: SQS and SNS interfaces are handled in Meerkat Drill, rewrite to reflect the changes
        """
        pass


