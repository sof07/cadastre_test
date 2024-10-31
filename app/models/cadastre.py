from sqlalchemy import Column, DateTime, String, func, Float

from app.core.db import Base


class Cadastre(Base):
    cadastral_number = Column(
        String,
        name='Кадастровый номер',
        max_length=20,
        nullable=False,
    )
    latitude = Column(
        Float,
        name='Широта',
        nullable=False,
    )
    longitude = Column(
        Float,
        name='Долгота',
        nullable=False,
    )
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f'Кадастровый номер {self.cadastral_number}'
