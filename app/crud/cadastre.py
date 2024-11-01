from app.crud.base import CRUDBase
from app.models.cadastre import Cadastre
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class CRUDCadastre(CRUDBase):
    async def get_multi_from_cadastre(
        self,
        cadastre_number: str,
        session: AsyncSession,
    ):
        db_objs = await session.execute(
            select(self.model).where(self.model.cadastre_number == cadastre_number)
        )
        return db_objs.scalars().all()


cadastre_crud = CRUDCadastre(Cadastre)
