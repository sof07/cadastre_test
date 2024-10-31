from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cadastre import CadastreBase, CadastreDB

from app.core.db import get_async_session

from app.crud.cadastre import cadastre_crud


router = APIRouter()


@router.post(
    '/query',
    response_model=CadastreDB,  # сериализатор для ответа
    summary='Получить запрос',
)
async def create_cadastre(
    session: AsyncSession = Depends(get_async_session),
) -> CadastreDB: ...


@router.get('/ping')
async def check_ping() -> bool: ...


@router.get('/history')
async def get_history(
    session: AsyncSession = Depends(get_async_session),
) -> list[CadastreDB]: ...


@router.post('/result')
async def server() -> bool: ...
