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
from meerkat_nest.country_config import demo_config

# Application config
#config_directory = os.environ("COUNTRY_CONFIG_DIR")

# Country config
#country_config_file = os.environ("COUNTRY_CONFIG")
country_config = demo_config.country_config

#spec = importlib.util.spec_from_file_location(
#    "country_config_module",
#    config_directory + country_config_file
#)
#country_config_module = importlib.util.module_from_spec(spec)
#spec.loader.exec_module(country_config_module)
#country_config = country_config_module.country_config
