from app.crud.base import CRUDBase
from app.models.cadastre import Cadastre
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDCadastre(CRUDBase): ...


cadastre_crud = CRUDCadastre(Cadastre)
