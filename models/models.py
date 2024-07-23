from sqlalchemy import String, Column, ForeignKey, Date, Integer
from sqlalchemy.orm import relationship

from core.configs import settings


# Tabela de funcionários
class Funcionario(settings.DBBaseModel):
    __tablename__ = 'funcionario' 

    cpf = Column(String(11), primary_key=True, unique=True, nullable=False)
    nome = Column(String(250))
    endereco = Column(String(250))
    estado = Column(String(250))
    data_nasc = Column(Date)
    rg = Column(String(12))
    telefone = Column(String(13))
    cod_banco = Column(String(4))
    nome_banco = Column(String(150), nullable=True)
    agencia = Column(String(6))
    conta_corrente = Column(String(14))
    matricula = Column(String(20))
    posto_trabalho = Column(String(250))
    cargo = Column(String(150))
    cidade = Column(String(250))
    centro_custo = Column(String(150))

# Tabela de estado
class Estado(settings.DBBaseModel):
    __tablename__ = 'estado'

    cod_estado = Column(Integer, primary_key=True, nullable=False)
    estado = Column(String(250), nullable=False)

    rel_cidade = relationship('Cidade', back_populates='rel_estado')

# Tabela de cidade
class Cidade(settings.DBBaseModel):
    __tablename__ = 'cidade'

    cod_municipio = Column(Integer, primary_key=True, nullable=False)
    cod_estado = Column(Integer, ForeignKey('estado.cod_estado', name='fk_cod_estado'), nullable=False)
    habitantes = Column(Integer, nullable=False)
    cidade = Column(String(250), nullable=False)

    rel_estado = relationship('Estado', back_populates='rel_cidade')

# Tabela de SD
class NumeroSd(settings.DBBaseModel):
    __tablename__ = 'numero_sd'
    
    ultimo_numero = Column(Integer, primary_key=True, default=0)
    
# Tabela de Bancos
class Banco(settings.DBBaseModel):
    __tablename__ = 'banco'
    
    cod_banco = Column(String(3), primary_key=True, nullable=False)
    nome_banco = Column(String(250), nullable=False)