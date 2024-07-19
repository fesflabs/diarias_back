from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.deps import get_session, validate_form_token
from models.models import Estado, Cidade
from schema.localidades_schema import EstadoResponse, CodEstadoRequest, CidadeNomeResponse

router = APIRouter()


@router.get("/estados", response_model=list[EstadoResponse])
async def get_estados(
    db: AsyncSession = Depends(get_session),
    user_id: str = Depends(validate_form_token)
):
    async with db as session:
        result = await session.execute(select(Estado))
        estados = result.scalars().all()
        if not estados:
            raise HTTPException(
                status_code=404, detail="Nenhum estado encontrado")
        return estados


@router.post("/cidades", response_model=list[CidadeNomeResponse])
async def get_cidades_por_estado(
    request: CodEstadoRequest,
    db: AsyncSession = Depends(get_session),
    user_id: str = Depends(validate_form_token)
):
    cod_estado = request.cod_estado

    async with db as session:
        result = await session.execute(
            select(Cidade.cidade).filter_by(cod_estado=cod_estado)
        )
        cidades = result.scalars().all()

        if not cidades:
            raise HTTPException(
                status_code=404, detail="Nenhuma cidade encontrada para este estado."
            )

        return [{"cidade": cidade} for cidade in cidades]
