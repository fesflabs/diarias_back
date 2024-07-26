from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.deps import get_session, validate_form_token
from models.models import Banco
from schema.banco_schema import BancoResponse

router = APIRouter()


@router.get("/listar", response_model=list[BancoResponse])
async def get_bancos(
    db: AsyncSession = Depends(get_session),
    user_id: str = Depends(validate_form_token)
):
    async with db as session:
        result = await session.execute(select(Banco))
        bancos = result.scalars().all()
        if not bancos:
            raise HTTPException(
                status_code=404, detail="Nenhum banco encontrado")
        return bancos
