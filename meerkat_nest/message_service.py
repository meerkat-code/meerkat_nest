"""
Data resource for interacting with Amazon Simple Queue Service
"""
import boto3
import json
import logging
import redis

from meerkat_nest import config

region_name = 'eu-west-1'
if hasattr(config, "LOCAL") and config.LOCAL:
    sqs_client = boto3.client('sqs', region_name=region_name,
                              endpoint_url=config.SQS_ENDPOINT)
else:
    sqs_client = boto3.client('sqs', region_name=region_name)
sts_client = boto3.client('sts', region_name=region_name)
sns_client = boto3.client('sns', region_name=region_name)
redis_ = redis.StrictRedis(host='redis', port=6379, db=0)
REDIS_QUEUE_NAME = 'nest-queue-' + config.country_config['country_name'].lower()


def get_account_id():
    """
    Returns AWS account ID
    
    Returns:\n
        account ID for the configured AWS user\n
    """
    if hasattr(config, "LOCAL") and config.LOCAL:
        return ""
    account_id = sts_client.get_caller_identity()["Account"]
    return account_id


def get_queue_name(data_entry):
    """
    Creates a queue name based on organization, entry content
    and entry subcontent

    Returns:\n
        automatically generated SQS queue name\n
    """
    return 'nest-queue-' + config.country_config['country_name'].lower()  # + '-'\
#           + data_entry['content'] + '-' + data_entry['formId']


def get_dead_letter_queue_name(data_entry):
    """
    Creates a dead letter queue name for an organization and content type
    
    Returns:\n
        automatically generated SQS queue name\n
    """
    return 'nest-dead-letter-queue-' + config.country_config['country_name'].lower()  # + '-' + data_entry['content']


def create_sns_topic():
    """
    Creates a SNS topic based on the country configurations

    Returns:\n
        Topic ARN
    """
    topic = sns_client.create_topic(
        Name='nest-incoming-topic-' + config.country_config['country_name'].lower()
    )

    return topic['TopicArn']


def get_queue_url(queue_name):
    """
    Creates a queue URL based on given queue name
    
    Returns:\n
        URL for the given queue\n
    """
    response = sqs_client.get_queue_url(
        QueueName=queue_name,
        QueueOwnerAWSAccountId=get_account_id()
    )
    return response['QueueUrl']


def create_queue(data_entry):
    """
    Creates a queue based on the given data entry
    """
    try:
        queue_name = get_queue_name(data_entry)
        response = sqs_client.create_queue(
            QueueName=queue_name
        )
        return response
    except Exception as e:
        message = e.args[0]
        message += "\Message queue creation failed."
        e.args = (message,)
        raise


def send_data(data_entry):
    """
    Sends data to a Redis queue which is later send to SQS in batches
    
    Returns:\n
        uuid for the PK of the raw data row\n
    """
    redis_.lpush(REDIS_QUEUE_NAME, json.dumps(data_entry))


def send_deactivation_message(data_entry):
    created = create_queue(data_entry)
    try:
        assert created, "Queue could not be created"
    except AssertionError as e:
        message = e.args[0]
        message += " Message queue creation failed."
        e.args = (message,)
        raise

    data_entry_delete = data_entry
    data_entry_delete['data'] = 'delete'
    response = sqs_client.send_message(
        QueueUrl=get_queue_url(get_queue_name(data_entry_delete)),
        MessageBody=json.dumps(data_entry)
    )
    logging.debug("SQS send message response " + str(response))

    notify_sns(get_queue_name(data_entry), get_dead_letter_queue_name(data_entry))

    return data_entry_delete


def receive_data(queue_name, n=1):
    return_set = []

    for i in range(0, n):
        return_set.append(sqs_client.receive_message(
                QueueUrl=get_queue_url(queue_name),
            )
        )
    return return_set


def notify_sns(queue_name, dead_letter_queue_name):
    """
    Notify Simple Notification service that queue has new data
    """
    message = {
        "queue": queue_name,
        "dead-letter-queue": dead_letter_queue_name
    }

    response = sns_client.publish(
        TopicArn=create_sns_topic(),
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )
    logging.debug("SNS notification response " + str(response))
