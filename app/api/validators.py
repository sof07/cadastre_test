from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.cadastre import Cadastre
from app.crud.cadastre import cadastre_crud


async def check_cadastre_number(
    cadastre_number: int,
    session: AsyncSession,
) -> Cadastre:
    """Проверяет существует ли кадастровый номер."""
    cadastre = await cadastre_crud.get_by_attribute(
        attr_name='cadastre_number',
        attr_value=cadastre_number,
        session=session,
    )
    if cadastre is None:
        raise HTTPException(status_code=404, detail='Кадастровый номер не найден!')
