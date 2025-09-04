from sqlalchemy import Column, ForeignKey, Table
from models.model_base import ModelBase

conservantes_picoles = Table(
    'conservantes_picoles',
    ModelBase.metadata,
    Column('id_conservante', ForeignKey('conservantes.id'), primary_key=True),
    Column('id_picole', ForeignKey('picoles.id'), primary_key=True)
)
