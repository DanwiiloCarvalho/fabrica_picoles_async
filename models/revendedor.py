from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, DateTime, String
from models.model_base import ModelBase
# from models.nota_fiscal import NotaFiscal

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.nota_fiscal import NotaFiscal


class Revendedor(ModelBase):
    __tablename__ = 'revendedores'

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False)

    cnpj: Mapped[str] = mapped_column(String(45), nullable=False)

    razao_social: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)

    contato: Mapped[str] = mapped_column(String(100), nullable=False)

    notas_fiscais: Mapped[list["NotaFiscal"]] = relationship(
        back_populates='revendedor', lazy='joined', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self) -> str:
        return f'<Revendedor: {self.razao_social}>'
