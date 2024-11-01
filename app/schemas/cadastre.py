from pydantic import BaseModel, validator, root_validator, Extra, Field
from datetime import datetime


class CadastreBase(BaseModel):
    cadastre_number: str = Field(example='00:00:0000:0000')
    latitude: float = Field(example=50.05681)
    longitude: float = Field(example=50.05681)


class CadastreUpdate(CadastreBase): ...


class CadastreCreate(CadastreBase):
    server_response: bool


class CadastreDB(CadastreCreate):
    created_at: datetime

    class Config:
        orm_mode = True
