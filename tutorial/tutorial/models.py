from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings
"""
retuns a Base class that all mapped classes
should inherit 
A class definition should have a Table and mapper() generated
"""
Base = declarative_base()

def db_connect():
    """
    Connects database using database settings from settings.py.
    Returns sqlalchemy engine
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    Base.metadata.create_all(engine)
"""
Create App_MetaData table from base
"""
class AppMetadata(Base):
    __tablename__ = "metadata"
    id = Column(Integer, primary_key=True)
    distributor = Column('distributor', Text)
    url = Column('url', Text)
    title = Column('title', Text)
    # date = Column('date', DateTime)
    developer = Column('developer', Text)
    titleXpath = Column('title_Xpath', Text)
    
    