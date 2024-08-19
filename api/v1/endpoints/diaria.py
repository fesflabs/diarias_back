from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session, validate_form_token
from schema.diaria_schema import Solicitacao, SDRequest
from utils.diarias_functions import (
    calcular_valores,
    verificar_duracao_total,
    validar_data,
    validar_hora,
)
from utils.sd_functions import gerar_numero_unico, gerar_data_hora_sd, validar_codigo_sd
from datetime import datetime, timedelta

router = APIRouter()


@router.post("/calcular")
async def calcular_diarias(
    request: Solicitacao,
    db: AsyncSession = Depends(get_session),
    user_id: str = Depends(validate_form_token),
):

    trechos = request.trechos
    tipo_sd = request.tipo_sd
    codigo_sd = request.codigo_sd
    valor_sd = request.valor_sd

    if not trechos:
        raise HTTPException(status_code=400, detail="Lista de trechos está vazia.")

    for trecho in trechos:
        dt_hr_saida = datetime.strptime(
            f"{trecho.dt_saida} {trecho.hr_saida}", "%d/%m/%Y %H:%M"
        )
        dt_hr_retorno = datetime.strptime(
            f"{trecho.dt_retorno} {trecho.hr_retorno}", "%d/%m/%Y %H:%M"
        )
        if dt_hr_saida > dt_hr_retorno:
            raise HTTPException(
                status_code=400,
                detail=f"A data/hora de saída não pode ser maior que a data/hora de retorno: {trecho.dt_saida} {trecho.hr_saida} - {trecho.dt_retorno} {trecho.hr_retorno} - {trecho.cidade_origem}/{trecho.cidade_destino}",
            )
        if not validar_data(trecho.dt_saida) or not validar_data(trecho.dt_retorno):
            raise HTTPException(
                status_code=400,
                detail=f"Formato de data inválido em um dos trechos: {trecho}",
            )
        if not validar_hora(trecho.hr_saida) or not validar_hora(trecho.hr_retorno):
            raise HTTPException(
                status_code=400,
                detail=f"Formato de hora inválido em um dos trechos: {trecho}",
            )
        if not trecho.cidade_origem or not trecho.cidade_destino:
            raise HTTPException(
                status_code=400, detail="Cidades de origem e destino são obrigatórias."
            )
        if not trecho.estado_origem or not trecho.estado_destino:
            raise HTTPException(
                status_code=400, detail="Estados de origem e destino são obrigatórios."
            )

    (
        quantidade_diarias_simples,
        quantidade_diarias_completas,
        valor_diarias_simples,
        valor_diarias_completas,
        valor_total,
    ) = await calcular_valores(trechos, db)

    match tipo_sd:
        case "solicitação":
            verificar_duracao_total(trechos)
            return {
                "quantidade_diarias_simples": quantidade_diarias_simples,
                "quantidade_diarias_completas": quantidade_diarias_completas,
                "valor_diarias_simples": round(valor_diarias_simples, 2),
                "valor_diarias_completas": round(valor_diarias_completas, 2),
                "valor_total": round(valor_total, 2),
                "user_id": user_id,
            }
        case "complementação":
            # Para complementação não tem limite de dias
            if not codigo_sd or valor_sd is None:
                raise HTTPException(
                    status_code=400,
                    detail="Campos 'codigo_sd' e 'valor_sd' são obrigatórios para complementação.",
                )
            if valor_sd >= valor_total:
                raise HTTPException(
                    status_code=400,
                    detail="O valor da solicitação deve ser menor que o valor total para complementação.",
                )
            if not validar_codigo_sd(codigo_sd):
                raise HTTPException(
                    status_code=400,
                    detail="Formato de 'codigo_sd' inválido. Deve ser 00000/ano.",
                )
            valor_complementacao = valor_total - valor_sd
            return {
                "quantidade_diarias_simples": quantidade_diarias_simples,
                "quantidade_diarias_completas": quantidade_diarias_completas,
                "valor_diarias_simples": round(valor_diarias_simples, 2),
                "valor_diarias_completas": round(valor_diarias_completas, 2),
                "valor_total": round(valor_total, 2),
                "valor_sd": round(valor_sd, 2),
                "valor_complementacao": round(valor_complementacao, 2),
                "user_id": user_id,
            }
        case "devolução":
            verificar_duracao_total(trechos)
            if not codigo_sd or valor_sd is None:
                raise HTTPException(
                    status_code=400,
                    detail="Campos 'codigo_sd' e 'valor_sd' são obrigatórios para devolução.",
                )
            if valor_sd <= valor_total:
                raise HTTPException(
                    status_code=400,
                    detail="O valor da solicitação deve ser maior que o valor total para devolução.",
                )
            if not validar_codigo_sd(codigo_sd):
                raise HTTPException(
                    status_code=400,
                    detail="Formato de 'codigo_sd' inválido. Deve ser 00000/ano.",
                )
            valor_devolucao = valor_sd - valor_total
            return {
                "quantidade_diarias_simples": quantidade_diarias_simples,
                "quantidade_diarias_completas": quantidade_diarias_completas,
                "valor_diarias_simples": round(valor_diarias_simples, 2),
                "valor_diarias_completas": round(valor_diarias_completas, 2),
                "valor_total": round(valor_total, 2),
                "valor_sd": round(valor_sd, 2),
                "valor_devolucao": round(valor_devolucao, 2),
                "user_id": user_id,
            }
        case _:
            raise HTTPException(status_code=400, detail="Tipo de solicitação inválido.")


@router.post("/gerar_sd")
async def gerar_sd(
    request: SDRequest,
    db: AsyncSession = Depends(get_session),
    user_id: str = Depends(validate_form_token),
):
    tipo_sd = request.tipo_sd
    codigo_sd = request.codigo_sd

    if tipo_sd not in ["solicitação", "complementação", "devolução"]:
        raise HTTPException(
            status_code=400,
            detail="Tipo de solicitação inválido. Use 'solicitação', 'complementação' ou 'devolução'.",
        )

    if tipo_sd == "solicitação":
        sd = await gerar_numero_unico(db)
        data_hora_sd = gerar_data_hora_sd()
    else:
        if not codigo_sd:
            raise HTTPException(
                status_code=400,
                detail="O parâmetro 'codigo_sd' é obrigatório para tipos 'complementação' e 'devolução'.",
            )
        if not validar_codigo_sd(codigo_sd):
            raise HTTPException(
                status_code=400,
                detail="Formato de 'codigo_sd' inválido. Deve ser 00000/ano.",
            )
        sd = codigo_sd
        data_hora_sd = None

    return {"codigo_sd": sd, "data_hora_sd": data_hora_sd, "user_id": user_id}
