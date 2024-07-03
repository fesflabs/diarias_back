from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema
from pydantic import BaseModel, EmailStr

from core.deps import get_session
from core.auth import criar_token_acesso_formulario

from sqlalchemy.ext.asyncio import AsyncSession

from core.configs import config

router = APIRouter()

class EmailSchema(BaseModel):
    email: EmailStr

@router.post('/enviar-link-acesso', status_code=status.HTTP_202_ACCEPTED)
async def enviar_link_acesso(email_schema: EmailSchema, db: AsyncSession = Depends(get_session)):
    email = email_schema.email

    if not email.endswith('@fesfsus.ba.gov.br'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas emails com o domínio @fesfsus.ba.gov.br são autorizados a receber o link de acesso."
        )

    # Simulando a criação do token sem armazenar o email no banco
    token = criar_token_acesso_formulario(sub=email)

    # Construir o link de acesso com o token JWT
    link_acesso = f"http://example.com/autenticacao?token={token}"

    # Preparar o corpo do email
    message = MessageSchema(
        subject='Link de Acesso ao Sistema de Diárias',
        recipients=[email],
        body=f"Olá,<br><br>"
             f"Você solicitou um link de acesso ao Sistema de Diárias. Clique no link abaixo para acessar:<br>"
             f"<a href='{link_acesso}'>{link_acesso}</a>",
        subtype='html'
    )

    # Enviar o email
    fm = FastMail(config)
    await fm.send_message(message)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Email enviado com sucesso."})
