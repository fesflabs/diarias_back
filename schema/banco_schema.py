from pydantic import BaseModel, Field


class BancoResponse(BaseModel):
    cod_banco: str
    nome_banco: str

    class Config:
        from_attributes = True
