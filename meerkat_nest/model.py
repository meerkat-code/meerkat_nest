"""
Database model definition
"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.event import listen

Base = declarative_base()


form_tables = {}

data_source_schemas = {[
    'odk':'ODK_RAW'
    ]}
odk_raw_schema = 'ODK_RAW'
staging_schema = 'STAGING'

for data_source in data_source_schemas:
    listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS " + data_source_schemas[data_source]))

listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS " + staging_schema))

class odkRawData(Base):
    __tablename__ = 'odk_raw_data'


    uuid = Column(String, primary_key=True)
    timestamp = Column(DateTime)
    token = Column(String)
    content = Column(String)
    formId = Column(String)
    formVersion = Column(String)
    data = Column(JSONB)


