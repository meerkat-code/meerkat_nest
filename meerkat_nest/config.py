"""
Configuration file for meerkat_nest

This configuration file sets up application level configurations
and imports the country specific configurations.

Many of the application level configurations can be overwritten by
environemental variables:

MEERKAT_NEST_DB_URL: db_url

COUNTRY_CONFIG_DIR: path to directory with country config

COUNTRY_CONFIG: name of country config file

"""
import os
import importlib.util
import logging
import random
import hashlib

# Application config
config_directory = os.environ.get("COUNTRY_CONFIG_DIR",
                   os.path.dirname(os.path.realpath(__file__)) + "/country_config/")

# Country config
country_config_file = os.environ.get("COUNTRY_CONFIG", "demo_config.py")
spec = importlib.util.spec_from_file_location(
    "country_config_module",
    config_directory + country_config_file
)
country_config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(country_config_module)
country_config = country_config_module.country_config


SEND_DATA_TO_SQS = os.environ.get("SEND_DATA_TO_SQS", True)

# Read salt from a file

salt_file = os.environ.get("SALT", "salt")

if salt_file:
    try:
        f = open(salt_file, 'r')
        salt = f.read()
        salt = salt.encode('utf-8')
    except FileNotFoundError as e:
        logging.warning("Salt file not found, creating it..")
        f_new = open(salt_file, 'w+')
        salt = hashlib.sha256(str(random.random()).encode('utf-8')).hexdigest()
        f_new.write(salt)
        f_new.close()

SQS_ENDPOINT = 'http://tunnel:9324'


class Config(object):
    DEBUG = True
    TESTING = False
    LOCAL = True


class Production(Config):
    DEBUG = False
    TESTING = False
    LOCAL = False


class Development(Config):
    DEBUG = True
    TESTING = True


class Testing(Config):
    DEBUG = False
    TESTING = True
