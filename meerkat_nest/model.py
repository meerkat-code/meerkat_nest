"""
Database model definition
"""
from sqlalchemy import Column, String, DateTime, DDL, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.event import listen

from meerkat_nest import config

Base = declarative_base()


data_type_tables = {}

for table in config.country_config["tables"]:
    data_type_tables[table] = type(table, (Base, ),
                              {"__tablename__": table,
                               "id": Column(Integer, primary_key=True),
                               "uuid": Column(String, index=True),
                               "data": Column(JSONB)})


class rawDataOdkCollect(Base):
    """
    ORM for raw data table for ODK form input
    """
    __tablename__ = 'raw_data_odk_collect'

    uuid = Column(String, primary_key=True)
    received_on = Column(DateTime)
    valid_from = Column(DateTime)
    authentication_token = Column(String)
    content = Column(String)
    formId = Column(String)
    formVersion = Column(String)
    data = Column(JSONB)

#class rawDataOdkCollectArchive(rawDataOdkCollect):



