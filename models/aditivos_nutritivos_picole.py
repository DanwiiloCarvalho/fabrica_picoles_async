from sqlalchemy import Column, ForeignKey, Table
from models.model_base import ModelBase


aditivos_nutritivos_picole = Table(
    'aditivos_nutritivos_picole',
    ModelBase.metadata,
    Column('id_aditivo_nutritivo', ForeignKey(
        'aditivos_nutritivos.id'), primary_key=True),
    Column('id_picole', ForeignKey(
        'picoles.id'), primary_key=True)
)
