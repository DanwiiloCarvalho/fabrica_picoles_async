"""
Forma antiga:

from sqlalchemy.ext.declarative import declarative_base

ModelBase = declarative_base()
"""
from sqlalchemy.orm import DeclarativeBase


class ModelBase(DeclarativeBase):
    pass
