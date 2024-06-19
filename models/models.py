import fastapi
from sqlalchemy import String, Column, Enum, ForeignKey, Date, Integer
from sqlalchemy.orm import validates, relationship

from core.configs import Settings

#tabela de funcionarios
class funcionario(Settings.DBBaseModel):
    cpf: str = Column(String(11), primary_key=True,unique= True ,nullable= False)
    nome:str = Column(String(250) )
    endereco: str = Column(String(250))
    estado: str = Column(String(50))
    data_nasc: Date = Column(Date)
    rg: str = Column(String(12))
    telefone:str = Column(String(11))
    cod_banco: str = Column(String(10), ForeignKey('registroBanco.cod_banco', nome= 'fk_cod_banco'))
    agencia: str = Column(String(10))
    conta_corrente:str= Column(String(10))
    matricula:str= Column(String(10))
    posto_trabalho:str= Column(String(10))
    cargo:str= Column(String(10))
    cidade: str= Column(String(10))
    centro_custo:str= Column(String(10))
#definindo relação entre colunas de banco e funcionario
    rel_registroBanco= relationship('models', back_populates='rel_funcionario')

#tabela de funcionarios
class registroBanco(Settings.DBBaseModel):
    cod_banco: str = Column(String(10), primary_key=True, unique=True, nullable=False)
    nome_banco: str = Column(String(50), nullable=True)

#definindo relação entre colunas de banco e funcionario
    rel_funcionario= relationship('models', back_populates= 'rel_registroBanco')


class estado(Settings.DBBaseModel):
    cod_estado: int = Column(Integer, primary_key=True ,nullable=False)
    estado: str = Column(String(50), nullable=False) 

    rel_cidade = relationship('models', back_populates='rel_estado')

class cidade(Settings.DBBaseModel):
    cod_municipio: str = Column(String(250), primary_key=True, nullable=False)
    cod_estado: int = Column(Integer, ForeignKey('estado.cod_estado', nome= 'fk_cod_estado'), nullable=False )
    habitantes: int = Column(Integer,nullable=False )
    cidade: str = Column(String(50), nullable=False,)

    rel_estado = relationship('models', back_populates='rel_cidade')
