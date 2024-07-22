from pydantic import BaseModel


class EstadoResponse(BaseModel):
    cod_estado: int
    estado: str

    class Config:
        from_attributes = True


class CodEstadoRequest(BaseModel):
    cod_estado: int


class CidadeNomeResponse(BaseModel):
    cidade: str

    class Config:
        from_attributes = True
