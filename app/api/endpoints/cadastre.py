from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cadastre import CadastreBase, CadastreDB, CadastreCreate

from app.core.db import get_async_session

from app.crud.cadastre import cadastre_crud
import httpx
import random


router = APIRouter()


@router.post(
    '/query',
    response_model=CadastreDB,
    summary='Получить запрос',
)
async def create_cadastre(
    cadastre: CadastreBase,
    session: AsyncSession = Depends(get_async_session),
) -> CadastreDB:
    response = await response_server()
    cadastre = CadastreCreate(**cadastre.dict(), **response)
    return await cadastre_crud.create(cadastre, session)


@router.get('/ping')
async def check_ping():
    return status.HTTP_200_OK


@router.get(
    '/history',
    response_model=list[CadastreDB],
    summary='Получить историю запросов',
)
async def get_history(
    session: AsyncSession = Depends(get_async_session),
) -> list[CadastreDB]:
    return await cadastre_crud.get_multi(session)


@router.get(
    '/history/{cadastre_number}/',
    response_model=list[CadastreDB],
    summary='Получить историю запросов по кадастровому номеру',
)
async def get_history_from_cadastre_number(
    cadastre_number,
    session: AsyncSession = Depends(get_async_session),
) -> list[CadastreDB]:
    return await cadastre_crud.get_multi_from_cadastre(
        cadastre_number,
        session,
    )


@router.get('/result')
async def server() -> dict:
    response = random.choice([True, False])
    return {'server_response': response}


async def response_server() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8000/result')
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail='Ошибка при получении данных'
            )
        item_data = response.json()
        return item_data
