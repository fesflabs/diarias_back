from fastapi import APIRouter

from api.v1.endpoints import funcionario, diaria, localidades

api_router = APIRouter()

api_router.include_router(funcionario.router, prefix='/funcionario', tags= ['funcionario'])
api_router.include_router(diaria.router, prefix='/diaria', tags=['diaria'])
api_router.include_router(localidades.router, prefix='/localidades', tags=['localidades'])