"""create tables for funcionario, registro_banco, estado, cidade, numero_sd

Revision ID: <your_revision_id>
Revises: 
Create Date: 2024-07-12 xx:xx:xx

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = '960907c2ae59'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Tabela de registro de banco
    op.create_table(
        'registro_banco',
        sa.Column('cod_banco', sa.String(length=3), primary_key=True, unique=True, nullable=False),
        sa.Column('num_banco', sa.String(length=3), nullable=True),
        sa.Column('nome_banco', sa.String(length=150), nullable=True)
    )

    # Tabela de estado
    op.create_table(
        'estado',
        sa.Column('cod_estado', sa.Integer, primary_key=True, nullable=False),
        sa.Column('estado', sa.String(length=250), nullable=False)
    )

    # Tabela de cidade
    op.create_table(
        'cidade',
        sa.Column('cod_municipio', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('cod_estado', sa.Integer, sa.ForeignKey('estado.cod_estado', name='fk_cod_estado'), nullable=False),
        sa.Column('habitantes', sa.Integer, nullable=False),
        sa.Column('cidade', sa.String(length=250), nullable=False)
    )

    # Tabela de funcionários
    op.create_table(
        'funcionario',
        sa.Column('cpf', sa.String(length=11), primary_key=True, unique=True, nullable=False),
        sa.Column('nome', sa.String(length=250)),
        sa.Column('endereco', sa.String(length=250)),
        sa.Column('estado', sa.String(length=250)),
        sa.Column('data_nasc', sa.Date),
        sa.Column('rg', sa.String(length=12)),
        sa.Column('telefone', sa.String(length=12)),
        sa.Column('cod_banco', sa.String(length=3), sa.ForeignKey('registro_banco.cod_banco', name='fk_cod_banco')),
        sa.Column('agencia', sa.String(length=6)),
        sa.Column('conta_corrente', sa.String(length=12)),
        sa.Column('matricula', sa.String(length=20)),
        sa.Column('posto_trabalho', sa.String(length=250)),
        sa.Column('cargo', sa.String(length=150)),
        sa.Column('cidade', sa.String(length=250)),
        sa.Column('centro_custo', sa.String(length=150))
    )

    # Tabela de SD
    op.create_table(
        'numero_sd',
        sa.Column('ultimo_numero', sa.Integer, primary_key=True, default=0)
    )

    # Inserindo dados de teste
    op.bulk_insert(
        sa.table(
            'registro_banco',
            sa.column('cod_banco', sa.String),
            sa.column('num_banco', sa.String),
            sa.column('nome_banco', sa.String)
        ),
        [
            {'cod_banco': '001', 'num_banco': '001', 'nome_banco': 'Banco do Brasil'},
            {'cod_banco': '237', 'num_banco': '237', 'nome_banco': 'Bradesco'},
            {'cod_banco': '341', 'num_banco': '341', 'nome_banco': 'Itaú'}
        ]
    )

    op.bulk_insert(
        sa.table(
            'estado',
            sa.column('cod_estado', sa.Integer),
            sa.column('estado', sa.String)
        ),
        [
            {'cod_estado': 1, 'estado': 'São Paulo'},
            {'cod_estado': 2, 'estado': 'Rio de Janeiro'},
            {'cod_estado': 3, 'estado': 'Minas Gerais'}
        ]
    )

    op.bulk_insert(
        sa.table(
            'cidade',
            sa.column('cod_municipio', sa.Integer),
            sa.column('cod_estado', sa.Integer),
            sa.column('habitantes', sa.Integer),
            sa.column('cidade', sa.String)
        ),
        [
            {'cod_municipio': 1, 'cod_estado': 1, 'habitantes': 1234567, 'cidade': 'São Paulo'},
            {'cod_municipio': 2, 'cod_estado': 2, 'habitantes': 654321, 'cidade': 'Rio de Janeiro'},
            {'cod_municipio': 3, 'cod_estado': 3, 'habitantes': 789012, 'cidade': 'Belo Horizonte'}
        ]
    )

    op.bulk_insert(
        sa.table(
            'funcionario',
            sa.column('cpf', sa.String),
            sa.column('nome', sa.String),
            sa.column('endereco', sa.String),
            sa.column('estado', sa.String),
            sa.column('data_nasc', sa.Date),
            sa.column('rg', sa.String),
            sa.column('telefone', sa.String),
            sa.column('cod_banco', sa.String),
            sa.column('agencia', sa.String),
            sa.column('conta_corrente', sa.String),
            sa.column('matricula', sa.String),
            sa.column('posto_trabalho', sa.String),
            sa.column('cargo', sa.String),
            sa.column('cidade', sa.String),
            sa.column('centro_custo', sa.String)
        ),
        [
            {'cpf': '12345678901', 'nome': 'João Silva', 'endereco': 'Rua A, 123', 'estado': 'São Paulo', 'data_nasc': datetime.date(1980, 1, 1), 'rg': '1234567', 'telefone': '11987654321', 'cod_banco': '001', 'agencia': '1234', 'conta_corrente': '123456-7', 'matricula': '12345', 'posto_trabalho': 'Escritório SP', 'cargo': 'Analista', 'cidade': 'São Paulo', 'centro_custo': 'TI'},
            {'cpf': '98765432100', 'nome': 'Maria Souza', 'endereco': 'Avenida B, 456', 'estado': 'Rio de Janeiro', 'data_nasc': datetime.date(1990, 2, 2), 'rg': '7654321', 'telefone': '21987654321', 'cod_banco': '237', 'agencia': '5678', 'conta_corrente': '987654-3', 'matricula': '67890', 'posto_trabalho': 'Escritório RJ', 'cargo': 'Desenvolvedor', 'cidade': 'Rio de Janeiro', 'centro_custo': 'Desenvolvimento'}
        ]
    )

    # Inserindo valor inicial na tabela numero_sd
    op.bulk_insert(
        sa.table(
            'numero_sd',
            sa.column('ultimo_numero', sa.Integer)
        ),
        [
            {'ultimo_numero': 0}
        ]
    )


def downgrade():
    op.drop_table('numero_sd')
    op.drop_table('funcionario')
    op.drop_table('cidade')
    op.drop_table('estado')
    op.drop_table('registro_banco')
