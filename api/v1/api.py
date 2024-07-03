from fastapi import APIRouter

from api.v1.endpoints import funcionario

api_router = APIRouter()

api_router.include_router(funcionario.router, prefix='/funcionario', tags= ['funcionario'])
