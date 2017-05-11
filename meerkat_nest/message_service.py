"""
Data resource for interacting with Amazon Simple Queue Service
"""
import boto3
import json
from meerkat_nest.util.create_queue_name import create_queue_name

sqs_client = boto3.client('sqs')
sts_client = boto3.client('sts')

def get_account_id():
    """
    Returns AWS account ID
    
    Returns:\n
        account ID for the configured AWS user\n
    """
    account_id = sts_client.get_caller_identity()["Account"]
    return account_id

def get_queue_url(queue_name):
    """
    Creates a queue URL based on given queue name
    
    Returns:\n
        URL for the given queue\n
    """
	response = client.get_queue_url(
    	QueueName=queue_name,
    	QueueOwnerAWSAccountId=get_account_id()
	)
	return response['QueueUrl']

def create_queue(data_entry):
    """
    Creates a queue based on the given data entry
    
    Returns:\n
        uuid for the PK of the raw data row\n
    """
    try:
        queue_name = create_queue_name(data_entry)
        return True
    except Exception e:
        print(e)
        return False

def send_data(data_entry):
    """
    Sends data to an Amazon Simple Message Service queue
    
    Returns:\n
        uuid for the PK of the raw data row\n
    """
    queue_name = create_queue_name(data_entry)
    try:
        response = sqs_client.send_message(
            QueueUrl=get_queue_url(create_queue_name(data_entry)),
            MessageBody=json.dumps(data_entry['data']),
            DelaySeconds=123
        )
        return True
    except Exception as e:
        print(e)
        return False