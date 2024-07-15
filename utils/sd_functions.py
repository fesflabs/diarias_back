from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import NumeroSd
from datetime import datetime

async def gerar_numero_unico(db: AsyncSession) -> str:
    result = await db.execute(select(NumeroSd).limit(1))
    numero_unico = result.scalars().first()

    if not numero_unico:
        # Cria um novo registro se não houver nenhum
        numero_unico = NumeroSd(ultimo_numero=1)
        db.add(numero_unico)
    else:
        numero_unico.ultimo_numero += 1

    await db.commit()
    await db.refresh(numero_unico)
    
    # Formata o número sequencial com 5 dígitos à esquerda com zeros
    numero_formatado = f"{numero_unico.ultimo_numero:05d}"
    
    # Obtém o ano atual
    ano_atual = datetime.now().year
    
    # Retorna o número único no formato desejado
    return f"{numero_formatado}/{ano_atual}"
