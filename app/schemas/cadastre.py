from pydantic import BaseModel, Field
from datetime import datetime


class CadastreBase(BaseModel):
    cadastre_number: str = Field(
        pattern=r'^\d{2}:\d{2}:\d{6,7}:\d{2}(:\d:\d)?$',
        example='00:00:0000000:00',
        description="""Кадастровый номер формат: ХХ:ХХ:ХХХХХХХ:ХХ:Х:Х 
        или  ХХ:ХХ:ХХХХХХХ:ХХ""",
        title='Кадастровый номер',
    )
    latitude: float = Field(
        ge=-90,
        le=90,
        example=50.05681,
        title='Широта',
    )
    longitude: float = Field(
        ge=-180,
        le=180,
        example=50.05681,
        title='Долгота',
    )


class CadastreCreate(CadastreBase):
    server_response: bool


class CadastreDB(CadastreCreate):
    created_at: datetime

    class Config:
        orm_mode = True
