from sqlalchemy.orm import Session
from .databases import SessionLocal, init_db
from . import models, crud, schemas

def init_data():
    db: Session = SessionLocal()
    init_db()  # Certifique-se de que as tabelas são criadas

    # Verifique se a tabela está vazia
    if db.query(models.ADCClientes).first() is None:
        cliente = schemas.ADCClientesCreate(
            NOME='VOLUS INSTITUICAO DE PAGAMENTO LTDA',
            USUARIO='TESTE',
            CEP=75901260,
            BAIRRO='SETOR CENTRAL',
            LOCALIDADE='ITUMBIARA',
            STATUS='A',
            FILIAL=600,
            NOME_FANTASIA='VOLUS TESTE FROTA'
        )
        crud.create_adc_cliente(db=db, cliente=cliente)

    db.close()

if __name__ == "__main__":
    init_data()
