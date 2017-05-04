"""
Database model definition
"""
from sqlalchemy import Column, String, DateTime, DDL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.event import listen

Base = declarative_base()

form_tables = {}

class rawDataOdkCollect(Base):
    __tablename__ = 'raw_data_odk_collect'

    uuid = Column(String, primary_key=True)
    timestamp = Column(DateTime)
    token = Column(String)
    content = Column(String)
    formId = Column(String)
    formVersion = Column(String)
    data = Column(JSONB)


