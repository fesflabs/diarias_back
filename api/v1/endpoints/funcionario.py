from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema

from pydantic import BaseModel, EmailStr

from core.deps import get_session
from core.auth import criar_token_acesso_formulario
from core.configs import config

from sqlalchemy import func, String
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import os

from schema.funcionario_schema import FuncionarioSchemaBase
from models.models import Funcionario

from datetime import datetime


load_dotenv()
link_acesso_base = os.getenv('LINK_ACESSO')

router = APIRouter()

class CPFSchema(BaseModel):
    cpf: str

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
    link_acesso = f"http://{link_acesso_base}?token={token}"

    # Preparar o corpo do email
    message = MessageSchema(
        subject='Link de Acesso ao Sistema de Diárias',
        recipients=[email],
        body=f"Olá,<br><br>"
             f"Você solicitou um link de acesso ao Sistema de Diárias. Clique no link abaixo para acessar:<br>"
             f"<a href='{link_acesso}'>Clique aqui para acessar o sistema</a>",
        subtype='html'
    )

    # Enviar o email
    fm = FastMail(config)
    await fm.send_message(message)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Email enviado com sucesso."})


@router.get('/buscar/', response_model=FuncionarioSchemaBase)
async def get_funcionario(cpf_schema: CPFSchema, 
                          db: AsyncSession = Depends(get_session)):
    cpf = cpf_schema.cpf

    async with db as session:
        query = select(Funcionario).filter(func.cast(Funcionario.cpf, String) == cpf)

        result = await session.execute(query)
        funcionarios = result.scalars().all()

        if not funcionarios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Funcionário com CPF {cpf} não encontrado"
            )

        funcionario = funcionarios[0]
        funcionario_dict = {
        **funcionario.__dict__,
        'data_nasc': (
            funcionario.data_nasc.strftime('%d/%m/%Y') 
            if isinstance(funcionario.data_nasc, datetime) 
            else None
        )
    }

        return funcionario_dict