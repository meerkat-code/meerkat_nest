"""
Data resource for interacting with Amazon Simple Queue Service
"""
import boto3
from meerkat_nest.util.create_queue_name import create_queue_name

client = boto3.client('sqs')

def send_data(data_entry):
    queue_name = create_queue_name(data_entry)
    try:
        response = client.create_queue(
            QueueName = queue_name
        )
        return True
    except Exception as e:
        return False