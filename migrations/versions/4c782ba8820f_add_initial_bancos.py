"""add initial bancos

Revision ID: 4c782ba8820f
Revises: f305d56b5a29
Create Date: 2024-07-23 10:03:26.800862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String

# revision identifiers, used by Alembic.
revision: str = '4c782ba8820f'
down_revision: Union[str, None] = 'f305d56b5a29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Define a tabela temporária para a inserção
banco_table = table('banco',
                    column('cod_banco', String),
                    column('nome_banco', String)
                    )


def upgrade():
    op.create_table(
        'banco',
        sa.Column('cod_banco', sa.String(length=3), nullable=False),
        sa.Column('nome_banco', sa.String(length=250), nullable=False),
        sa.PrimaryKeyConstraint('cod_banco')
    )

    bancos = [
        {'cod_banco': '001', 'nome_banco': 'Banco do Brasil'},
        {'cod_banco': '033', 'nome_banco': 'Banco Santander'},
        {'cod_banco': '070', 'nome_banco': 'Banco de Brasília'},
        {'cod_banco': '104', 'nome_banco': 'Caixa Econômica'},
        {'cod_banco': '237', 'nome_banco': 'Banco Bradesco'},
        {'cod_banco': '341', 'nome_banco': 'Banco Itaú'},
        {'cod_banco': '077', 'nome_banco': 'Banco Inter'},
        {'cod_banco': '136', 'nome_banco': 'Unicred'},
        {'cod_banco': '748', 'nome_banco': 'Sicredi'},
        {'cod_banco': '004', 'nome_banco': 'Banco do Nordeste'},
        {'cod_banco': '290', 'nome_banco': 'Banco PagSeguro'},
        {'cod_banco': '623', 'nome_banco': 'Banco PAN'},
        {'cod_banco': '323', 'nome_banco': 'Banco Mercado Pago'},
        {'cod_banco': '536', 'nome_banco': 'Banco Neon'},
        {'cod_banco': '756', 'nome_banco': 'Banco Bancoob'},
        {'cod_banco': '380', 'nome_banco': 'Banco Pic Pay'},
        {'cod_banco': '041', 'nome_banco': 'Banrisul'},
        {'cod_banco': '260', 'nome_banco': 'Nubank'},
        {'cod_banco': '336', 'nome_banco': 'Banco C6 bank'},
        {'cod_banco': '765', 'nome_banco': 'SICOOB'}
    ]

    op.bulk_insert(banco_table, bancos)


def downgrade():
    op.drop_table('banco')
