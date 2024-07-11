from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date
from datetime import datetime
from typing import Sequence, Union

revision: str = '755c826c5004'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Create estado table
    op.create_table(
        'estado',
        sa.Column('cod_estado', Integer, primary_key=True),
        sa.Column('estado', String(250), nullable=False)
    )

    # Create registroBanco table
    op.create_table(
        'registroBanco',
        sa.Column('cod_banco', String(3), primary_key=True),
        sa.Column('num_banco', String(3), nullable=False),
        sa.Column('nome_banco', String(150), nullable=False)
    )

    # Create cidade table
    op.create_table(
        'cidade',
        sa.Column('cod_municipio', Integer, primary_key=True),
        sa.Column('cod_estado', Integer, sa.ForeignKey('estado.cod_estado')),
        sa.Column('habitantes', Integer),
        sa.Column('cidade', String(250), nullable=False)
    )

    # Create funcionario table
    op.create_table(
        'funcionario',
        sa.Column('cpf', String(11), primary_key=True),
        sa.Column('nome', String(250), nullable=False),
        sa.Column('endereco', String(250), nullable=False),
        sa.Column('estado', String(250), nullable=False),
        sa.Column('data_nasc', Date, nullable=False),
        sa.Column('rg', String(12), nullable=False),
        sa.Column('telefone', String(12), nullable=False),
        sa.Column('cod_banco', String(3), sa.ForeignKey('registroBanco.cod_banco')),
        sa.Column('agencia', String(6), nullable=False),
        sa.Column('conta_corrente', String(12), nullable=False),
        sa.Column('matricula', String(20), nullable=False),
        sa.Column('posto_trabalho', String(250), nullable=False),
        sa.Column('cargo', String(150), nullable=False),
        sa.Column('cidade', String(250), nullable=False),
        sa.Column('centro_custo', String(150), nullable=False)
    )

    # Insert initial data into estado table
    estado_table = table('estado',
                         column('cod_estado', Integer),
                         column('estado', String(250))
                         )

    estados = [
        {'cod_estado': 11, 'estado': 'RO'},
        {'cod_estado': 12, 'estado': 'AC'},
        {'cod_estado': 13, 'estado': 'AM'},
        {'cod_estado': 14, 'estado': 'RR'},
        {'cod_estado': 15, 'estado': 'PA'},
        {'cod_estado': 16, 'estado': 'AP'},
        {'cod_estado': 17, 'estado': 'TO'},
        {'cod_estado': 21, 'estado': 'MA'},
        {'cod_estado': 22, 'estado': 'PI'},
        {'cod_estado': 23, 'estado': 'CE'},
        {'cod_estado': 24, 'estado': 'RN'},
        {'cod_estado': 25, 'estado': 'PB'},
        {'cod_estado': 26, 'estado': 'PE'},
        {'cod_estado': 27, 'estado': 'AL'},
        {'cod_estado': 28, 'estado': 'SE'},
        {'cod_estado': 29, 'estado': 'BA'},
        {'cod_estado': 31, 'estado': 'MG'},
        {'cod_estado': 32, 'estado': 'ES'},
        {'cod_estado': 33, 'estado': 'RJ'},
        {'cod_estado': 35, 'estado': 'SP'},
        {'cod_estado': 41, 'estado': 'PR'},
        {'cod_estado': 42, 'estado': 'SC'},
        {'cod_estado': 43, 'estado': 'RS'},
        {'cod_estado': 50, 'estado': 'MS'},
        {'cod_estado': 51, 'estado': 'MT'},
        {'cod_estado': 52, 'estado': 'GO'},
        {'cod_estado': 53, 'estado': 'DF'},
    ]

    op.bulk_insert(estado_table, estados)

    # Insert initial data into registroBanco table
    registroBanco_table = table('registroBanco',
                                column('cod_banco', String(3)),
                                column('num_banco', String(3)),
                                column('nome_banco', String(150))
                                )

    bancos = [
        {'cod_banco': '001', 'num_banco': '001', 'nome_banco': 'Banco do Brasil'},
        {'cod_banco': '237', 'num_banco': '237', 'nome_banco': 'Bradesco'},
        {'cod_banco': '341', 'num_banco': '341', 'nome_banco': 'Itaú'},
    ]

    op.bulk_insert(registroBanco_table, bancos)

    # Insert initial data into cidade table
    cidade_table = table('cidade',
                         column('cod_municipio', Integer),
                         column('cod_estado', Integer),
                         column('habitantes', Integer),
                         column('cidade', String(250))
                         )

    cidades = [
        {'cod_municipio': 1, 'cod_estado': 35, 'habitantes': 123456, 'cidade': 'São Paulo'},
        {'cod_municipio': 2, 'cod_estado': 33, 'habitantes': 654321, 'cidade': 'Rio de Janeiro'},
    ]

    op.bulk_insert(cidade_table, cidades)

    # Insert initial data into funcionario table
    funcionario_table = table('funcionario',
                              column('cpf', String(11)),
                              column('nome', String(250)),
                              column('endereco', String(250)),
                              column('estado', String(250)),
                              column('data_nasc', Date),
                              column('rg', String(12)),
                              column('telefone', String(12)),
                              column('cod_banco', String(3)),
                              column('agencia', String(6)),
                              column('conta_corrente', String(12)),
                              column('matricula', String(20)),
                              column('posto_trabalho', String(250)),
                              column('cargo', String(150)),
                              column('cidade', String(250)),
                              column('centro_custo', String(150))
                              )

    funcionarios = [
        {'cpf': '12345678901', 'nome': 'João Silva', 'endereco': 'Rua A, 123', 'estado': 'SP', 'data_nasc': datetime.strptime('1980-01-01', '%Y-%m-%d').date(),
         'rg': '123456789', 'telefone': '11999999999', 'cod_banco': '001', 'agencia': '1234', 'conta_corrente': '123456',
         'matricula': '123456', 'posto_trabalho': 'Central', 'cargo': 'Médico', 'cidade': 'São Paulo', 'centro_custo': 'Saúde'},
        {'cpf': '98765432100', 'nome': 'Maria Oliveira', 'endereco': 'Rua B, 456', 'estado': 'RJ', 'data_nasc': datetime.strptime('1990-02-02', '%Y-%m-%d').date(),
         'rg': '987654321', 'telefone': '21999999999', 'cod_banco': '237', 'agencia': '5678', 'conta_corrente': '654321',
         'matricula': '654321', 'posto_trabalho': 'Unidade 1', 'cargo': 'Enfermeira', 'cidade': 'Rio de Janeiro', 'centro_custo': 'Saúde'},
    ]

    op.bulk_insert(funcionario_table, funcionarios)


def downgrade():
    op.drop_table('funcionario')
    op.drop_table('cidade')
    op.drop_table('registroBanco')
    op.drop_table('estado')
