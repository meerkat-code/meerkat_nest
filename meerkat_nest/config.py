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
