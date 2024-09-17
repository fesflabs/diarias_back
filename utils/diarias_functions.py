from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import Cidade
from fastapi import HTTPException
import re

# Valores das diárias em um dicionário
VALORES_DIARIAS = {
    "diaria_completa_fora_estado": 360,
    "diaria_completa_estado_pequena": 180,
    "diaria_completa_estado_grande": 270,
    "diaria_simples_fora_estado": 180,
    "diaria_simples_estado_pequena": 90,
    "diaria_simples_estado_grande": 135,
}

CODIGO_BAHIA = 29
LIMITE_HABITANTES = 100000

cidades_sem_diaria = [
    "Lauro de Freitas", "Simões Filho", "Camaçari", "Dias d'Ávila",
    "Mata de São João", "Vera Cruz", "Itaparica", "Candeias",
    "São Francisco do Conde", "Madre de Deus", "São Sebastião do Passé"
]


async def get_cidade_info(cidade_nome: str, estado: int, db: AsyncSession):
    result = await db.execute(select(Cidade).filter(Cidade.cidade == cidade_nome, Cidade.cod_estado == estado))
    cidade = result.scalars().first()
    if cidade:
        return {
            "estado": cidade.cod_estado,
            "habitantes": cidade.habitantes
        }
    return None


async def calcular_valores(trechos, db):
    quantidade_diarias_simples = 0
    quantidade_diarias_completas = 0
    valor_diarias_simples = 0
    valor_diarias_completas = 0
    valor_total = 0

    # Verificar duração total dos trechos
    if len(trechos) > 1:
        dt_saida_primeiro_trecho = datetime.strptime(
            f"{trechos[0].dt_saida} {trechos[0].hr_saida}", "%d/%m/%Y %H:%M")
        dt_retorno_ultimo_trecho = datetime.strptime(
            f"{trechos[-1].dt_retorno} {trechos[-1].hr_retorno}", "%d/%m/%Y %H:%M")
        total_duracao = dt_retorno_ultimo_trecho - dt_saida_primeiro_trecho

        if total_duracao > timedelta(hours=8) and total_duracao.days < 1:
            quantidade_diarias_simples += 1
            trecho = trechos[-1]
            cidade_destino_info = await get_cidade_info(trecho.cidade_origem, trecho.estado_origem, db)
            if cidade_destino_info:
                estado_destino = cidade_destino_info["estado"]
                habitantes = cidade_destino_info["habitantes"]
                if estado_destino != CODIGO_BAHIA:
                    valor_diarias_simples += VALORES_DIARIAS["diaria_simples_fora_estado"]
                    valor_total += VALORES_DIARIAS["diaria_simples_fora_estado"]
                else:
                    if habitantes < LIMITE_HABITANTES:
                        valor_diarias_simples += VALORES_DIARIAS["diaria_simples_estado_pequena"]
                        valor_total += VALORES_DIARIAS["diaria_simples_estado_pequena"]
                    else:
                        valor_diarias_simples += VALORES_DIARIAS["diaria_simples_estado_grande"]
                        valor_total += VALORES_DIARIAS["diaria_simples_estado_grande"]
            else:
                raise HTTPException(status_code=404, detail=f"Cidade {trecho.cidade_destino} no estado {trecho.estado_destino} não encontrada")
            return quantidade_diarias_simples, quantidade_diarias_completas, valor_diarias_simples, valor_diarias_completas, valor_total

    # Calcular valores das diárias para cada trecho individualmente
    for i, trecho in enumerate(trechos):
        dt_saida = datetime.strptime(
            f"{trecho.dt_saida} {trecho.hr_saida}", "%d/%m/%Y %H:%M")
        dt_retorno = datetime.strptime(
            f"{trecho.dt_retorno} {trecho.hr_retorno}", "%d/%m/%Y %H:%M")
        dt_retorno_ultimo_trecho = datetime.strptime(
            f"{trechos[-1].dt_retorno}", "%d/%m/%Y")

        cidade_destino_info = await get_cidade_info(trecho.cidade_destino, trecho.estado_destino, db)
        # Se tiver mais de um trecho, no ultimo trecho a cidade de origem passa a entrar em vigor no calculo e não a cidade de destino
        if i == len(trechos) - 1 and len(trechos) > 1:
            cidade_destino_info = await get_cidade_info(trecho.cidade_origem, trecho.estado_origem, db)

        if cidade_destino_info:
            estado_destino = cidade_destino_info["estado"]
            habitantes = cidade_destino_info["habitantes"]

            if estado_destino == CODIGO_BAHIA and trecho.cidade_origem == 'Salvador' and trecho.cidade_destino in cidades_sem_diaria:
                continue

            dias_viagem = (dt_retorno.date() - dt_saida.date()).days
            if dias_viagem > 0:
                quantidade_diarias_completas += dias_viagem
                for _ in range(dias_viagem):
                    if estado_destino != CODIGO_BAHIA:
                        valor_diarias_completas += VALORES_DIARIAS["diaria_completa_fora_estado"]
                        valor_total += VALORES_DIARIAS["diaria_completa_fora_estado"]
                    else:
                        if habitantes < LIMITE_HABITANTES:
                            valor_diarias_completas += VALORES_DIARIAS["diaria_completa_estado_pequena"]
                            valor_total += VALORES_DIARIAS["diaria_completa_estado_pequena"]
                        else:
                            valor_diarias_completas += VALORES_DIARIAS["diaria_completa_estado_grande"]
                            valor_total += VALORES_DIARIAS["diaria_completa_estado_grande"]
            elif (dt_retorno - dt_saida) > timedelta(hours=8):
                # Não contabilizar diária simples caso tiver uma diária completa nos próximos trechos
                if dt_retorno_ultimo_trecho > dt_retorno:
                    continue
                quantidade_diarias_simples += 1
                if estado_destino != CODIGO_BAHIA:
                    valor_diarias_simples += VALORES_DIARIAS["diaria_simples_fora_estado"]
                    valor_total += VALORES_DIARIAS["diaria_simples_fora_estado"]
                else:
                    if habitantes < LIMITE_HABITANTES:
                        valor_diarias_simples += VALORES_DIARIAS["diaria_simples_estado_pequena"]
                        valor_total += VALORES_DIARIAS["diaria_simples_estado_pequena"]
                    else:
                        valor_diarias_simples += VALORES_DIARIAS["diaria_simples_estado_grande"]
                        valor_total += VALORES_DIARIAS["diaria_simples_estado_grande"]
        else:
            raise HTTPException(status_code=404, detail=f"Cidade {trecho.cidade_destino} no estado {trecho.estado_destino} não encontrada")

    return quantidade_diarias_simples, quantidade_diarias_completas, valor_diarias_simples, valor_diarias_completas, valor_total


def verificar_duracao_total(trechos):
    dt_saida_primeiro_trecho = datetime.strptime(
        f"{trechos[0].dt_saida} {trechos[0].hr_saida}", "%d/%m/%Y %H:%M")
    dt_retorno_ultimo_trecho = datetime.strptime(
        f"{trechos[-1].dt_retorno} {trechos[-1].hr_retorno}", "%d/%m/%Y %H:%M")
    total_dias = (dt_retorno_ultimo_trecho.date() -
                  dt_saida_primeiro_trecho.date()).days

    if total_dias > 8:
        raise HTTPException(
            status_code=400, detail="A duração total dos trechos não pode exceder 8 dias.")


def validar_data(data: str) -> bool:
    return bool(re.match(r"\d{2}/\d{2}/\d{4}", data))


def validar_hora(hora: str) -> bool:
    return bool(re.match(r"\d{2}:\d{2}", hora))
