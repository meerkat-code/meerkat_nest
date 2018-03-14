import meerkat_nest
import meerkat_nest.message_service
from meerkat_nest import app

from meerkat_nest.test.test_data.upload_payload import upload_payload

import boto3
import unittest
import logging
import json


class MeerkatNestPipelineTest(unittest.TestCase):
    """
    Comprehensive Test Case class for testing the whole Nest pipeline up to message queue.

    Note that a test payload will be delivered into the downstream message queue.
    """

    @classmethod
    def setup_class(cls):
        """Setup for testing"""

        app.config.from_object('config.Testing')

        # Only show warning level+ logs from boto3, botocore and nose.
        # Too verbose otherwise.
        logging.getLogger('boto3').setLevel(logging.WARNING)
        logging.getLogger('botocore').setLevel(logging.WARNING)

    def setUp(self):
        self.app = meerkat_nest.app.test_client()
        self.queue_name = 'nest-queue-demo-record-dem_test'
        self.dead_letter_queue_name = 'nest-dead-letter-queue-demo-record-dem-test'
        self.topic = 'nest-incoming-topic-demo'
        self.topic_arn = 'aws123:nest-incoming-topic-demo'
        self.data_entry = upload_payload

        region_name = 'eu-west-1'
        self.sqs_client = boto3.client('sqs', region_name=region_name)
        self.sts_client = boto3.client('sts', region_name=region_name)
        self.sns_client = boto3.client('sns', region_name=region_name)

    def tearDown(self):
        pass

    def test_upload(self):
        """
        Post a payload read from test_data/upload_payload.py to the app's Upload interface and check it gets processed
        correctly
        """
        payload = upload_payload
        uuid = upload_payload['data'][0]['instanceID']
        post_response = self.app.post('/upload',
                                      data=json.dumps(payload),
                                      headers={'Content-Type': 'application/json'})

        self.assertEqual(post_response.status_code, 200)

        # check that data ended up in queue
#        queue_name = meerkat_nest.message_service.get_queue_name(payload)
#        return_set = meerkat_nest.message_service.receive_data(queue_name, n=1)

#        form_payload = json.loads(return_set[0]['Messages'][0]['Body'])
#        uuid_from_sqs = form_payload['data']['instanceID']

        # TODO: send receipt for SQS

#        self.assertEqual(uuid, uuid_from_sqs)

        # check SNS via email

        # TODO: check data row in persistent database

        # check data in the Abacus queue
