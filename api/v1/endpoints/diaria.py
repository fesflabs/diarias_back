from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.deps import get_session
from schema.diaria_schema import Trecho
from utils.diarias_functions import calcular_valores, verificar_duracao_total

router = APIRouter()

@router.post("/calcular")
async def calcular_diarias(trechos: List[Trecho], db: AsyncSession = Depends(get_session)):
    if not trechos:
        raise HTTPException(status_code=400, detail="Lista de trechos está vazia.")
    
    verificar_duracao_total(trechos)
    diarias_completas, diarias_simples, valor_total = await calcular_valores(trechos, db)

    return {
        "diarias_completas": diarias_completas,
        "diarias_simples": diarias_simples,
        "valor_total": valor_total,
        "sd": '12345/2024'
    }
