__author__ = 'yutongpang'
import settings
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(URL(**settings.DATABASE))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Category(DeclarativeBase):
    __tablename__ = 'refractiveindexdatabase_category'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    elements = relationship('Element')


class Element(DeclarativeBase):
    __tablename__ = 'refractiveindexdatabase_element'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('refractiveindexdatabase_category.id'))
    category = relationship('Category')
    title = Column(String, unique=True)
    elementlist = relationship('Elementlist')


class Elementlist(DeclarativeBase):
    __tablename__ = 'refractiveindexdatabase_elementlist'
    id = Column(Integer, primary_key=True)
    element_id = Column(Integer, ForeignKey('refractiveindexdatabase_element.id'))
    element = relationship('Element')
    title = Column(String)
    references = Column(String, default='')
    comments = Column(String, default='')
    type = Column(String)
    datalink = Column(String)
    data = Column(JSON)
