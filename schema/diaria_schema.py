from pydantic import BaseModel
from typing import List, Optional


class Trecho(BaseModel):
    dt_saida: str
    hr_saida: str
    dt_retorno: str
    hr_retorno: str
    estado_origem: int
    estado_destino: int
    cidade_origem: str
    cidade_destino: str


class Solicitacao(BaseModel):
    trechos: List[Trecho]
    tipo_sd: str
    eh_curador: bool
    codigo_sd: Optional[str] = None
    valor_sd: Optional[float] = None


class SDRequest(BaseModel):
    tipo_sd: str
    codigo_sd: Optional[str] = None