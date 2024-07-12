from pydantic import BaseModel

class Trecho(BaseModel):
    dt_saida: str
    hr_saida: str
    dt_retorno: str
    hr_retorno: str
    estado_origem: int
    estado_destino: int
    cidade_origem: str
    cidade_destino: str
