from sqlalchemy import Column, ForeignKey, Table
from models.model_base import ModelBase


ingredientes_picole = Table(
    'ingredientes_picole',
    ModelBase.metadata,
    Column('id_ingrediente', ForeignKey('ingredientes.id'), primary_key=True),
    Column('id_picole', ForeignKey('picoles.id'), primary_key=True)
)
