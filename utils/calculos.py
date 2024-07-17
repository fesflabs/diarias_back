from typing import List
from pydantic import BaseModel, validator
from datetime import datetime, timedelta

class Viagem(BaseModel):
    cidade_origem: str
    cidade_destino: str
    data_inicio: datetime
    data_fim: datetime

    @property
    def calcular_diaria(self) -> float:
        # Lógica de cálculo de diária baseado na população das cidades
        diaria_base = 100  # Valor base da diária
        pop_origem = self.get_populacao(self.cidade_origem)
        pop_destino = self.get_populacao(self.cidade_destino)

        if pop_origem is None or pop_destino is None:
            raise ValueError("População não encontrada para uma das cidades")

        valor_diaria = diaria_base * ((pop_origem + pop_destino) / 10000)
        dias_viagem = (self.data_fim - self.data_inicio).days + 1
        return valor_diaria * dias_viagem

    def get_populacao(self, cidade: str) -> int:
        # Simulação de busca da população da cidade no banco de dados ou cache
        # Aqui, usaremos uma simulação simples baseada em dicionário para exemplo
        populacao_cidades = {
            "São Paulo": 12000000,
            "Rio de Janeiro": 6500000,
            "Belo Horizonte": 2500000,
            "Brasília": 3100000,
            "Salvador": 2900000,
        }
        return populacao_cidades.get(cidade)

    @validator('data_inicio', 'data_fim', pre=True)
    def parse_date(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v)
        return v

    @validator('data_fim', always=True)
    def check_data_fim(cls, v, values, **kwargs):
        if 'data_inicio' in values and v < values['data_inicio']:
            raise ValueError('A data de fim não pode ser anterior à data de início')
        return v
