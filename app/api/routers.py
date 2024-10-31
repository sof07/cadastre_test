from fastapi import APIRouter

# Две длинных строчки импортов заменяем на одну короткую.
from app.api.endpoints import cadastre

main_router = APIRouter()
main_router.include_router(cadastre, tags=['Cadastre'])
