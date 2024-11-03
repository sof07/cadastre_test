from sqlalchemy import Boolean, Column, DateTime, Float, String, func

from app.core.db import Base


class Cadastre(Base):
    cadastre_number = Column(
        String,
        name='Кадастровый номер',
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
    server_response = Column(Boolean)

    def __repr__(self):
        return f'Кадастровый номер {self.cadastral_number}'
