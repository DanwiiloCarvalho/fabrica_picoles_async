from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, DateTime, String
from models.model_base import ModelBase
# from models.picole import Picole
from models.conservantes_picoles import conservantes_picoles

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.picole import Picole


class Conservante(ModelBase):
    __tablename__ = 'conservantes'

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False)

    nome: Mapped[str] = mapped_column(String(45), nullable=False, unique=True)

    descricao: Mapped[str] = mapped_column(String(45), nullable=False)

    picoles: Mapped[list["Picole"]] = relationship(
        secondary=conservantes_picoles, back_populates='conservantes', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Conservante: {self.nome}>'
