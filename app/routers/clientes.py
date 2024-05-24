from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..databases import get_db
from .. import models, schemas, crud

router = APIRouter()

@router.get("/api/clientes/", response_model=list[schemas.ADCClientes])
def read_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clientes = db.query(models.ADCClientes).offset(skip).limit(limit).all()
    return clientes

@router.post("/api/clientes/", response_model=schemas.ADCClientes)
def create_cliente(cliente: schemas.ADCClientesCreate, db: Session = Depends(get_db)):
    return crud.create_cliente(db=db, cliente=cliente)

@router.put("/api/clientes/{cliente_id}", response_model=schemas.ADCClientes)
def update_cliente(cliente_id: int, cliente: schemas.ADCClientesUpdate, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud.update_cliente(db=db, cliente=db_cliente, cliente_update=cliente)

@router.delete("/api/clientes/{cliente_id}", response_model=schemas.ADCClientes)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud.delete_cliente(db=db, cliente=db_cliente)
