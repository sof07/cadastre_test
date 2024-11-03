from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.cadastre import Cadastre, cadastre_crud


async def check_cadastre_number(
    cadastre_number: int,
    session: AsyncSession,
) -> Cadastre:
    """
    Проверяет, существует ли кадастровый номер в базе данных.

    :param cadastre_number: Кадастровый номер, который необходимо проверить.
    :param session: Асинхронная сессия для выполнения запросов к базе данных.
    :return: Объект Cadastre, если кадастровый номер найден в базе данных.

    :raises HTTPException: Исключение возникает, если кадастровый номер не найден (404).
    """
    cadastre = await cadastre_crud.get_by_attribute(
        attr_name='cadastre_number',
        attr_value=cadastre_number,
        session=session,
    )
    if cadastre is None:
        raise HTTPException(status_code=404, detail='Кадастровый номер не найден!')
