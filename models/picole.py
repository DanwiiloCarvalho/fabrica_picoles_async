from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric
from models.model_base import ModelBase
from models.tipo_picole import TipoPicole
from models.sabor import Sabor
from models.tipo_embalagem import TipoEmbalagem
from models.ingrediente import Ingrediente
from models.ingredientes_picole import ingredientes_picole
from models.conservante import Conservante
from models.conservantes_picoles import conservantes_picoles
from models.aditivos_nutritivos_picole import aditivos_nutritivos_picole

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.aditivo_nutritivo import AditivoNutritivo


class Picole(ModelBase):
    __tablename__ = 'picoles'

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False)

    preco: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)

    id_sabor: Mapped[int] = mapped_column(
        ForeignKey('sabores.id'), nullable=False)
    sabor: Mapped[Sabor] = relationship(
        back_populates='picoles', lazy='joined')

    id_tipo_embalagem: Mapped[int] = mapped_column(
        ForeignKey('tipos_embalagem.id'), nullable=False)
    tipo_embalagem: Mapped[TipoEmbalagem] = relationship(
        back_populates='picoles', lazy='joined')

    id_tipo_picole: Mapped[int] = mapped_column(
        ForeignKey('tipos_picole.id'), nullable=False)
    tipo_picole: Mapped[TipoPicole] = relationship(
        back_populates='picoles', lazy='joined')

    aditivos_nutritivos: Mapped[list["AditivoNutritivo"] | None] = relationship(secondary=aditivos_nutritivos_picole,
                                                                                back_populates='picoles', lazy='joined')

    conservantes: Mapped[list[Conservante] | None] = relationship(
        secondary=conservantes_picoles, back_populates='picoles', lazy='joined')

    ingredientes: Mapped[list[Ingrediente]] = relationship(
        secondary=ingredientes_picole, back_populates='picoles', lazy='joined')

    def __repr__(self) -> str:
        return f'<Picole: {self.tipo_picole.nome} com sabor {self.sabor.nome} e preço {self.preco}>'
