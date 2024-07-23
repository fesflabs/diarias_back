from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema

from core.deps import get_session, validate_form_token
from core.auth import criar_token_acesso_formulario
from core.configs import config

from sqlalchemy import func, String
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import os

from schema.funcionario_schema import FuncionarioSchemaBase, EmailSchema, FuncionarioSchemaUp
from models.models import Funcionario
from utils.classes import FuncionarioCPF


load_dotenv()
link_acesso_base = os.getenv('LINK_ACESSO')

router = APIRouter()



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


@router.get('/buscar/{cpf}', response_model=FuncionarioSchemaBase)
async def get_funcionario(cpf: str,
                          db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Funcionario).filter(func.cast(Funcionario.cpf, String) == cpf)
        result = await session.execute(query)
        funcionario = result.scalars().first()
        if not funcionario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Funcionário com CPF {cpf} não encontrado"
            )

        funcionario_dict = {
            **funcionario.__dict__,
            'data_nasc': funcionario.data_nasc.strftime('%d/%m/%Y') if funcionario.data_nasc else None
        }

        return funcionario_dict
    

@router.put('/atualizar/', response_model=FuncionarioSchemaUp)
async def update_funcionario(update_data: FuncionarioSchemaUp,
                             db: AsyncSession = Depends(get_session),
                          user_id: str = Depends(validate_form_token)):
    cpf = update_data.cpf

    async with db as session:
        query = select(Funcionario).filter(func.cast(Funcionario.cpf, String) == cpf)
        result = await session.execute(query)
        funcionario = result.scalars().first()

        if not funcionario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Funcionário com CPF {cpf} não encontrado"
            )

        if update_data.cod_banco is not None:
            funcionario.cod_banco = update_data.cod_banco
        if update_data.nome_banco is not None:
            funcionario.nome_banco = update_data.nome_banco
        if update_data.agencia is not None:
            funcionario.agencia = update_data.agencia
        if update_data.conta_corrente is not None:
            funcionario.conta_corrente = update_data.conta_corrente

        await session.commit()
        await session.refresh(funcionario)

        return {
            "cpf": funcionario.cpf,
            "cod_banco": funcionario.cod_banco,
            "nome_banco": funcionario.nome_banco,
            "agencia": funcionario.agencia,
            "conta_corrente": funcionario.conta_corrente
        }
