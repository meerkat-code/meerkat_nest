"""
Meerkat Nest utility functions
"""
from meerkat_nest import config
import hashlib


def scramble(value):
    """
    scrambles the input string value

    Returns:\n
        Returns an empty string
    """
    ret = ''
    return ret


def hash(value):
    encrypted_value = hashlib.sha256(value.encode('utf-8')).hexdigest()

    return encrypted_value


def validate_request(data_entry):
    """
    Validates the data entry as supported input
    
    Returns:\n
        True if processing was successful, False otherwise
    """
    valid_data_structure = config.country_config['supported_content']

    try:
        if "authentication_token" in config.country_config.keys():
            assert data_entry['token'] == config.country_config["authentication_token"]
        assert 'content' in data_entry.keys(), "Content not defined" 
        assert data_entry['content'] in valid_data_structure.keys(),\
            "Content '" + data_entry['content'] + "' not supported"
        for key in valid_data_structure[data_entry['content']].keys():
            assert key in data_entry.keys(), "Key " + str(key) + " required" 
 
    except AssertionError as e:
        message = e.args[0]
        message += "\nRequest validation failed."
        e.args = (message,)
        raise


def raw_odk_data_to_dict(data_object):

    data_dict = {
        "uuid": data_object.uuid,
        "received_on": str(data_object.received_on),
        "active_from": str(data_object.active_from),
        "authentication_token": data_object.authentication_token,
        "content": data_object.content,
        "formId": data_object.formId,
        "formVersion": data_object.formVersion,
        "data": data_object.data
    }

    return data_dict
