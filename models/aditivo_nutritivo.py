from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, DateTime, String
from models.model_base import ModelBase
from models.picole import Picole
from models.aditivos_nutritivos_picole import aditivos_nutritivos_picole


class AditivoNutritivo(ModelBase):
    __tablename__ = 'aditivos_nutritivos'

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(45), nullable=False)

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False)

    formula_quimica: Mapped[str] = mapped_column(String(45), nullable=False)

    picoles: Mapped[list[Picole]] = relationship(
        secondary=aditivos_nutritivos_picole, back_populates='aditivos_nutritivos', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Aditivo Nutritivo -> nome: {self.nome} | Fórmula química: {self.formula_quimica}>'
