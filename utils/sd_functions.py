from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import NumeroSd
from datetime import datetime
import re


async def gerar_numero_unico(db: AsyncSession) -> str:
    result = await db.execute(select(NumeroSd).limit(1))
    numero_unico = result.scalars().first()

    if not numero_unico:
        numero_unico = NumeroSd(ultimo_numero=1)
        db.add(numero_unico)
    else:
        numero_unico.ultimo_numero += 1

    await db.commit()
    await db.refresh(numero_unico)

    numero_formatado = f"{numero_unico.ultimo_numero:05d}"
    ano_atual = datetime.now().year

    return f"{numero_formatado}/{ano_atual}"


def gerar_data_hora_sd():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def validar_codigo_sd(codigo: str) -> bool:
    return bool(re.match(r"^\d{5}/\d{4}$", codigo))
