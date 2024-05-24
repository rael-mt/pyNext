from sqlalchemy.orm import Session
from . import models, schemas
from typing import List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.CreateUser):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_adc_cliente(db: Session, cliente: models.ADCClientes):
    db_cliente = models.ADCClientes(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def get_users_all(db: Session, user: schemas.CreateUser):
    db_user = models.User(username=user.username, password=user.password)
    return db.query(db_user)

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_centro_custo(db: Session, centro_custo: schemas.FROCentroCustoCreate):
    db_centro_custo = models.FROCentroCusto(**centro_custo.dict())
    db.add(db_centro_custo)
    db.commit()
    db.refresh(db_centro_custo)
    return db_centro_custo

def get_centro_custos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.FROCentroCusto).offset(skip).limit(limit).all()

def get_centro_custo(db: Session, centro_custo_id: int):
    return db.query(models.FROCentroCusto).filter(models.FROCentroCusto.codigo == centro_custo_id).first()

def update_centro_custo(db: Session, centro_custo: models.FROCentroCusto, centro_custo_update: schemas.FROCentroCustoCreate):
    for key, value in centro_custo_update.dict().items():
        setattr(centro_custo, key, value)
    db.commit()
    db.refresh(centro_custo)
    return centro_custo

def delete_centro_custo(db: Session, centro_custo: models.FROCentroCusto):
    db.delete(centro_custo)
    db.commit()
    return centro_custo

def create_departamento(db: Session, departamento: schemas.FRODepartamentoCreate):
    db_departamento = models.FRODepartamento(**departamento.dict())
    db.add(db_departamento)
    db.commit()
    db.refresh(db_departamento)
    return db_departamento

def get_departamentos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.FRODepartamento).offset(skip).limit(limit).all()

def get_departamento(db: Session, departamento_id: int):
    return db.query(models.FRODepartamento).filter(models.FRODepartamento.codigo == departamento_id).first()

def update_departamento(db: Session, departamento: models.FRODepartamento, departamento_update: schemas.FRODepartamentoCreate):
    for key, value in departamento_update.dict().items():
        setattr(departamento, key, value)
    db.commit()
    db.refresh(departamento)
    return departamento

def delete_departamento(db: Session, departamento: models.FRODepartamento):
    db.delete(departamento)
    db.commit()
    return departamento

def get_departamentos_by_centro_custo(db: Session, centro_custo_id: int) -> List[models.FRODepartamento]:
    return db.query(models.FRODepartamento).filter(models.FRODepartamento.codigo_centro_custo == centro_custo_id).all()