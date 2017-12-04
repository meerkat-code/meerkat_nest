"""
Database model definition
"""
from sqlalchemy import Column, String, DateTime, DDL, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.event import listen

from meerkat_nest import config

Base = declarative_base()


data_type_tables = {}

for table in config.country_config["tables"]:
    if table in config.country_config["rename_forms"]:
        data_type_tables[table] = type(table, (Base, ),
                                  {"__tablename__": config.country_config["rename_forms"][table],
                                   "id": Column(Integer, primary_key=True),
                                   "uuid": Column(String, index=True),
                                   "data": Column(JSONB)})
    else:
        data_type_tables[table] = type(table, (Base,),
                                       {"__tablename__": table,
                                        "id": Column(Integer, primary_key=True),
                                        "uuid": Column(String, index=True),
                                        "data": Column(JSONB)})


class RawDataOdkCollect(Base):
    """
    ORM for raw data table for ODK form input
    """
    __tablename__ = 'raw_data_odk_collect'

    uuid = Column(String, primary_key=True)
    received_on = Column(DateTime, nullable=False)
    active_from = Column(DateTime, nullable=False)
    active_until = Column(DateTime)
    replaced_by = Column(String)
    authentication_token = Column(String)
    content = Column(String, nullable=False)
    formId = Column(String)
    formVersion = Column(String)
    data = Column(JSONB)




