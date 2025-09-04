from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Numeric, String, Table
from models.model_base import ModelBase
from models.revendedor import Revendedor
from models.lotes_nota_fiscal import lotes_nota_fiscal

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.lote import Lote


class NotaFiscal(ModelBase):
    __tablename__ = 'notas_fiscais'

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False)

    data: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    valor: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)

    numero_serie: Mapped[str] = mapped_column(
        String(45), nullable=False, unique=True)

    descricao: Mapped[str] = mapped_column(String(200), nullable=False)

    id_revendedor: Mapped[int] = mapped_column(
        ForeignKey('revendedores.id'), nullable=False)
    revendedor: Mapped[Revendedor] = relationship(
        back_populates='notas_fiscais', lazy='joined')

    lotes: Mapped[list["Lote"]] = relationship(
        secondary=lotes_nota_fiscal, back_populates='notas_fiscais', lazy='joined')

    def __repr__(self) -> str:
        return f'<Nota Fiscal: {self.numero_serie}>'
