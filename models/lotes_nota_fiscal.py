from sqlalchemy import Column, ForeignKey, Table
from models.model_base import ModelBase

lotes_nota_fiscal = Table(
    'lotes_nota_fiscal',
    ModelBase.metadata,
    Column('id_lote', ForeignKey('lotes.id'), primary_key=True),
    Column('id_nota_fiscal', ForeignKey('notas_fiscais.id'), primary_key=True)
)
