from pydantic import BaseModel
from typing import Optional


class RegistroBancoSchemaBase(BaseModel):
    cod_banco: str
    nome_banco: str

    class Config:
        from_attributes = True


class RegistroBancoSchemaUp(RegistroBancoSchemaBase):
    cod_banco: Optional[str] = None
    nome_banco: Optional[str] = None
