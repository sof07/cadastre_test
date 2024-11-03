import asyncio
import random

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_cadastre_number
from app.core.db import get_async_session
from app.crud.cadastre import cadastre_crud
from app.schemas.cadastre import CadastreBase, CadastreCreate, CadastreDB

router = APIRouter()
SERVER_URL = 'http://localhost:8000/result'
SERVER_RESPONSE_WAITING_TIME = 60.0


@router.post(
    '/query',
    response_model=CadastreDB,
    summary='Отправить запрос на сервер',
)
async def create_cadastre(
    cadastre: CadastreBase,
    session: AsyncSession = Depends(get_async_session),
):
    response = await response_server(SERVER_URL, **cadastre.dict())
    server_response_dict = {'server_response': response}
    cadastre = CadastreCreate(**cadastre.dict(), **server_response_dict)
    return await cadastre_crud.create(cadastre, session)


@router.get(
    '/ping',
    summary='Проверка готовности сервера',
)
async def check_ping():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(SERVER_URL)
        except httpx.ReadTimeout:
            raise HTTPException(
                status_code=504, detail='Время ожидания ответа от сервера истекло.'
            )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail='Сервер не готов'
            )
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
    cadastre_number: str,
    session: AsyncSession = Depends(get_async_session),
) -> list[CadastreDB]:
    await check_cadastre_number(cadastre_number, session)
    return await cadastre_crud.get_multi_from_cadastre(
        cadastre_number,
        session,
    )


@router.post('/result')
async def server(params: CadastreBase | None = None) -> bool:
    await asyncio.sleep(random.randint(1, 60))
    response = random.choice([True, False])
    return response


@router.get(
    '/result',
    include_in_schema=False,
)
async def response() -> int:
    return status.HTTP_200_OK


async def response_server(server_url, **kwargs) -> dict:
    """
    Отправляет асинхронный POST-запрос на указанный сервер.

    :param server_url: URL сервера, к которому будет отправлен запрос.
    :param kwargs: Дополнительные параметры, которые будут отправлены в теле запроса в формате JSON.
    :return: Словарь, содержащий данные, полученные от сервера (в формате JSON).

    :raises HTTPException: Исключение возникает, если время ожидания ответа истекает (504) или если
                          сервер возвращает код статуса, отличный от 200.
    """
    url = server_url
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                json=kwargs,
                timeout=SERVER_RESPONSE_WAITING_TIME,
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
