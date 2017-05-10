"""
Creates a name for a SQS messaging queue
"""

def create_queue_name(data_entry):
	return 'nest_queue_' + data_entry['content'] + '_' + data_entry['formId']