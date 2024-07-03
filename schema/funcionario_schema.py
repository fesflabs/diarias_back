from pydantic import BaseModel, validator
from sqlalchemy import Date
from typing import Optional
from utils.classes import FuncionarioFormatCpf

class FuncionarioSchemaBase(BaseModel):
    cpf = str
    nome = str
    endereco = str
    estado = str
    data_nasc = Date
    rg = str
    telefone = str
    cod_banco = str
    agencia = str
    conta_corrente = str
    matricula = str
    cargo = str
    cidade = str    
    centro_custo = str

    class Config:
        from_attributes = True


class FuncionarioSchemaUp(FuncionarioSchemaBase):
    cpf: Optional[str] = None
    nome: Optional [str] = None
    endereco: Optional [str] = None
    estado: Optional [str] = None
    data_nasc: Optional [Date] = None
    rg: Optional [str] = None
    telefone: Optional [str] = None
    cod_banco: Optional [str] = None
    agencia: Optional [str] = None
    conta_corrente: Optional [str] = None
    matricula: Optional [str] = None
    cargo: Optional [str] = None
    cidade: Optional [str] = None
    centro_custo: Optional [str] = None

    @validator('cpf')
    def validate_and_format_cpf(cls, cpf):
        return FuncionarioFormatCpf(cpf=cpf).validateCpf(key="cpf", cpf=cpf)
