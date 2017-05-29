"""
Meerkat Nest utility functions
"""
from meerkat_nest import config


def scramble(value):
	"""
	scrambles the input string value
	"""
	ret = ''
	return ret

def format_form_field_key(value):
	"""
	formats the field name
	"""
	ret = value.replace('-','/')

	return ret

def validate_request(data_entry):
    """
    Validates the data entry as supported input
    
    Returns:\n
        True if processing was successful, False otherwise
    """
    valid_data_structure = config.country_config['supported_content']

    try:
        assert 'content' in data_entry.keys(), "Content not defined" 
        assert data_entry['content'] in valid_data_structure.keys(), "Content '" + data_entry['content'] + "'' not supported"
 
    except AssertionError as e:
        message = e.args[0]
        message += "\nRequest validation failed."
        e.args = (message,)
        raise