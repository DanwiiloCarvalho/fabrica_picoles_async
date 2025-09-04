from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from models.model_base import ModelBase
# from models.picole import Picole
from models.ingredientes_picole import ingredientes_picole

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.picole import Picole


class Ingrediente(ModelBase):
    __tablename__ = 'ingredientes'

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False)

    nome: Mapped[str] = mapped_column(String(45), nullable=False, unique=True)

    picoles: Mapped[list["Picole"]] = relationship(
        secondary=ingredientes_picole, back_populates='ingredientes', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Ingredientes: {self.nome}>'
