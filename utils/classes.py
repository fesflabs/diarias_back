from pydantic import BaseModel, validator,Field
from validate_docbr import CPF
import re

class FuncionarioCPF(BaseModel):
    cpf: str = Field(..., min_length=11, max_length=11)

    @validator('cpf')
    def validar_cpf(cls, cpf: str) -> str:
        cpf_numerico = re.sub(r'\D', '', cpf)
        cpf_validator = CPF()
        if cpf_validator.validate(cpf_numerico):
            return cpf_numerico
        else:
            raise ValueError('CPF inválido')  
