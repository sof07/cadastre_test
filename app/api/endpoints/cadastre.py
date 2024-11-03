from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cadastre import CadastreBase, CadastreDB, CadastreCreate

from app.core.db import get_async_session
import asyncio
from app.crud.cadastre import cadastre_crud
from app.api.validators import check_cadastre_number

import httpx
import random


router = APIRouter()
URL = 'http://localhost:8000/result'


@router.post(
    '/query',
    response_model=CadastreDB,
    summary='Отправить запрос на сервер',
)
async def create_cadastre(
    cadastre: CadastreBase,
    session: AsyncSession = Depends(get_async_session),
) -> CadastreDB:
    response = await response_server(URL, **cadastre.dict())
    cadastre = CadastreCreate(**cadastre.dict(), **response)
    return await cadastre_crud.create(cadastre, session)


@router.get(
    '/ping',
    summary='Проверка готовности сервера',
)
async def check_ping():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8000/result')
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail='Сервер не готов'
            )
        return 'Сервер готов'


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
    cadastre_number: str,
    session: AsyncSession = Depends(get_async_session),
) -> list[CadastreDB]:
    await check_cadastre_number(cadastre_number, session)
    return await cadastre_crud.get_multi_from_cadastre(
        cadastre_number,
        session,
    )


@router.get('/result')
async def server() -> dict:
    await asyncio.sleep(random.randint(1, 60))
    response = random.choice([True, False])
    return {'server_response': response}


async def response_server(url, **kwargs) -> dict:
    url = url
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                timeout=60.0,
            )
        except httpx.ReadTimeout:
            raise HTTPException(
                status_code=504, detail='Время ожидания ответа от сервера истекло.'
            )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail='Ошибка при получении данных'
            )
        item_data = response.json()
        return item_data
