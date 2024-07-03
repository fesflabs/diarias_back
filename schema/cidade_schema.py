from typing import Optional

from pydantic import BaseModel


class CidadeSchemaBase(BaseModel):
    cod_municipio: str
    cod_estado: int
    habitantes: int
    cidade: str


    class Config:
        from_attributes = True


class EstadoSchemaUp(CidadeSchemaBase):
    cod_municipio: Optional[str] = None
    cod_estado: Optional[int]= None
    habitantes: Optional[int] = None
    cidade: Optional[str] = None
