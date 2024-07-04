from pydantic import BaseModel
from sqlalchemy.orm import validates
import re


class FuncionarioFormatCpf(BaseModel):
    cpf: str

    @validates('cpf')
    def validateCpf(self, key, cpf):
        cpf_numerico = re.sub(r'\D', '', cpf)
        return cpf_numerico
