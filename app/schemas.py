from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class CreateUser(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenData(BaseModel):
    username: str | None = None

class ADCClientesBase(BaseModel):
    NOME: str
    USUARIO: str
    CEP: int
    BAIRRO: str
    LOCALIDADE: str
    STATUS: str
    FILIAL: int
    NOME_FANTASIA: str

    class Config:
        from_attributes = True

class ADCClientesCreate(ADCClientesBase):
    pass

class ADCClientes(ADCClientesBase):
    CODIGO: int

    class Config:
        from_attributes = True
    
class ADCClientesUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None

    class Config:
        from_attributes = True

# schemas.py

from pydantic import BaseModel
from typing import Optional

class FROCentroCustoBase(BaseModel):
    descricao: str
    filial: int
    cliente: int

class FROCentroCustoCreate(FROCentroCustoBase):
    pass

class FROCentroCusto(FROCentroCustoBase):
    codigo: int

    class Config:
        from_attributes = True

class FRODepartamentoBase(BaseModel):
    filial: int
    cliente: int
    departamento: str
    cnpj: str
    razao_social: str
    nome_fantasia: str
    bairro: str
    cidade: str
    estado: str
    codigo_centro_custo: int

class FRODepartamentoCreate(FRODepartamentoBase):
    pass

class FRODepartamento(FRODepartamentoBase):
    codigo: int
    # centro_custo_codigo: int

    class Config:
        from_attributes = True
