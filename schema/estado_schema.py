from typing import Optional

from pydantic import BaseModel


class EstadoSchemaBase(BaseModel):
    cod_estado: int
    estado: str

    class Config:
        from_attributes = True


class EstadoSchemaUp(EstadoSchemaBase):
    cod_estado: Optional[str] = None
    estado: Optional[str] = None
