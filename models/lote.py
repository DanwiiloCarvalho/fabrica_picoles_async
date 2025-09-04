from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer
from models.model_base import ModelBase
###
# from models.tipo_picole import TipoPicole
###
from typing import TYPE_CHECKING
from models.nota_fiscal import NotaFiscal
from models.lotes_nota_fiscal import lotes_nota_fiscal

if TYPE_CHECKING:
    from models.tipo_picole import TipoPicole


class Lote(ModelBase):
    __tablename__ = 'lotes'

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False)

    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)

    id_tipo_picole: Mapped[int] = mapped_column(
        ForeignKey('tipos_picole.id'), nullable=False)
    tipo_picole: Mapped["TipoPicole"] = relationship(
        back_populates='lotes', lazy='joined')

    notas_fiscais: Mapped[list[NotaFiscal]
                          ] = relationship(secondary=lotes_nota_fiscal, back_populates='lotes', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Lote: {self.id}>'
