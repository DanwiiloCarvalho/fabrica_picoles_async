from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, DateTime, String
from models.model_base import ModelBase
from models.lote import Lote
# from models.picole import Picole

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.picole import Picole


class TipoPicole(ModelBase):
    __tablename__ = 'tipos_picole'

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False)

    nome: Mapped[str] = mapped_column(String(45), nullable=False)

    lotes: Mapped[list[Lote]] = relationship(back_populates='tipo_picole')

    picoles: Mapped[list["Picole"]] = relationship(
        back_populates='tipo_picole')

    def __repr__(self) -> str:
        return f'<Tipos Picolé: {self.nome}>'
