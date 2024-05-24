from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .databases import Base

class FROCentroCusto(Base):
    __tablename__ = "fro_centro_custo"

    codigo = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)
    filial = Column(Integer)
    cliente = Column(Integer)

    departamentos = relationship("FRODepartamento", back_populates="centro_custo")

class FRODepartamento(Base):
    __tablename__ = "fro_departamentos"

    codigo = Column(Integer, primary_key=True, index=True)
    filial = Column(Integer)
    cliente = Column(Integer)
    departamento = Column(String)
    cnpj = Column(String(18))
    razao_social = Column(String)
    nome_fantasia = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    estado = Column(String(2))
    centro_custo_codigo = Column(Integer, ForeignKey("fro_centro_custo.codigo"))
    codigo_centro_custo = Column(Integer)

    centro_custo = relationship("FROCentroCusto", back_populates="departamentos")

class ADCClientes(Base):
    __tablename__ = 'ADC_CLIENTES'

    CODIGO = Column(Integer, primary_key=True, index=True)
    NOME = Column(String, index=True)
    USUARIO = Column(String, index=True)
    CEP = Column(Integer)
    BAIRRO = Column(String)
    LOCALIDADE = Column(String)
    STATUS = Column(String)
    FILIAL = Column(Integer)
    NOME_FANTASIA = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
