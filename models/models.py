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
    agencia: str
    conta_corrente:str
    matricula:str
    posto_trabalho:str
    cargo:str
    cidade: str
    centro_custo:str

