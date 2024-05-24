from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, databases

router = APIRouter()

@router.post("/api/centros-custo/", response_model=schemas.FROCentroCusto)
def create_centro_custo(centro_custo: schemas.FROCentroCustoCreate, db: Session = Depends(databases.get_db)):
    return crud.create_centro_custo(db=db, centro_custo=centro_custo)

@router.get("/api/centros-custo/", response_model=List[schemas.FROCentroCusto])
def read_centros_custo(skip: int = 0, limit: int = 10, db: Session = Depends(databases.get_db)):
    centros_custo = crud.get_centro_custos(db, skip=skip, limit=limit)
    return centros_custo

@router.put("/api/centros-custo/{centro_custo_id}", response_model=schemas.FROCentroCusto)
def update_centro_custo(centro_custo_id: int, centro_custo: schemas.FROCentroCustoCreate, db: Session = Depends(databases.get_db)):
    db_centro_custo = crud.get_centro_custo(db, centro_custo_id=centro_custo_id)
    if db_centro_custo is None:
        raise HTTPException(status_code=404, detail="Centro de custo não encontrado")
    return crud.update_centro_custo(db=db, centro_custo=db_centro_custo, centro_custo_update=centro_custo)

@router.delete("/api/centros-custo/{centro_custo_id}", response_model=schemas.FROCentroCusto)
def delete_centro_custo(centro_custo_id: int, db: Session = Depends(databases.get_db)):
    db_centro_custo = crud.get_centro_custo(db, centro_custo_id=centro_custo_id)
    if db_centro_custo is None:
        raise HTTPException(status_code=404, detail="Centro de custo não encontrado")
    return crud.delete_centro_custo(db=db, centro_custo=db_centro_custo)

@router.post("/api/departamentos/", response_model=schemas.FRODepartamento)
def create_departamento(departamento: schemas.FRODepartamentoCreate, db: Session = Depends(databases.get_db)):
    return crud.create_departamento(db=db, departamento=departamento)

@router.get("/api/departamentos/", response_model=List[schemas.FRODepartamento])
def read_departamentos(skip: int = 0, limit: int = 10, db: Session = Depends(databases.get_db)):
    departamentos = crud.get_departamentos(db, skip=skip, limit=limit)
    return departamentos

@router.put("/api/departamentos/{departamento_id}", response_model=schemas.FRODepartamento)
def update_departamento(departamento_id: int, departamento: schemas.FRODepartamentoCreate, db: Session = Depends(databases.get_db)):
    db_departamento = crud.get_departamento(db, departamento_id=departamento_id)
    if db_departamento is None:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    return crud.update_departamento(db=db, departamento=db_departamento, departamento_update=departamento)

@router.delete("/api/departamentos/{departamento_id}", response_model=schemas.FRODepartamento)
def delete_departamento(departamento_id: int, db: Session = Depends(databases.get_db)):
    db_departamento = crud.get_departamento(db, departamento_id=departamento_id)
    if db_departamento is None:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    return crud.delete_departamento(db=db, departamento=db_departamento)

@router.get("/api/departamentos/centro-custo/{centro_custo_id}", response_model=List[schemas.FRODepartamento])
def get_departamentos_by_centro_custo(centro_custo_id: int, db: Session = Depends(databases.get_db)):
    departamentos = crud.get_departamentos_by_centro_custo(db, centro_custo_id)
    if not departamentos:
        raise HTTPException(status_code=404, detail="Nenhum departamento encontrado para este centro de custo")
    return departamentos