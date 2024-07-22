from pydantic import BaseModel
from sqlalchemy.orm import validates
import re

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calcular_digito(dados: str) -> int:
        soma = sum(int(dados[i]) * (10 - i) for i in range(9))
        resto = (soma * 10) % 11
        return resto if resto < 10 else 0

    digito1 = calcular_digito(cpf[:9])
    digito2 = calcular_digito(cpf[:9] + str(digito1))
    
    return cpf[-2:] == f"{digito1}{digito2}"

class FuncionarioFormatCpf(BaseModel):
    cpf: str

    @validates('cpf')
    def validateCpf(self, key, cpf):
        cpf_numerico = re.sub(r'\D', '', cpf)
        if not validar_cpf(cpf_numerico):
            raise ValueError("CPF inválido")
        return cpf_numerico
