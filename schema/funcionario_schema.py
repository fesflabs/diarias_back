from pydantic import BaseModel, validator
from typing import Optional
from utils.classes import FuncionarioFormatCpf


class FuncionarioSchemaBase(BaseModel):
    cpf: str
    nome: Optional[str]
    endereco: Optional[str]
    estado: Optional[str]
    data_nasc: Optional[str]
    rg: Optional[str]
    telefone: Optional[str]
    cod_banco: Optional[str]
    nome_banco: Optional[str]
    agencia: Optional[str]
    conta_corrente: Optional[str]
    matricula: Optional[str]
    posto_trabalho: Optional[str]
    cargo: Optional[str]
    cidade: Optional[str]
    centro_custo: Optional[str]

    class Config:
        orm_mode = True

    @validator('cpf')
    def validate_and_format_cpf(cls, cpf):
        # Replace FuncionarioFormatCpf with your actual validation logic
        if not FuncionarioFormatCpf(cpf=cpf).validateCpf(key="cpf", cpf=cpf):
            raise ValueError('CPF inválido')
        return cpf
