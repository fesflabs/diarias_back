from pydantic import BaseModel, Field


class EstadoResponse(BaseModel):
    cod_estado: int
    estado: str

    class Config:
        orm_mode = True


class CodEstadoRequest(BaseModel):
    cod_estado: int


class CidadeNomeResponse(BaseModel):
    cidade: str

    class Config:
        orm_mode = True
