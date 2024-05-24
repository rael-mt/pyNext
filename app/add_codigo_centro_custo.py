# update_db.py

from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy.exc import OperationalError

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Conecte-se ao banco de dados
with engine.connect() as connection:
    # Reflete a tabela existente
    fro_departamentos = Table("fro_departamentos", metadata, autoload_with=engine)

    # Verifique se a coluna já existe para evitar duplicação
    if not hasattr(fro_departamentos.c, 'codigo_centro_custo'):
        try:
            # Adicione a nova coluna
            connection.execute("ALTER TABLE fro_departamentos ADD COLUMN codigo_centro_custo INTEGER")
            print("Coluna 'codigo_centro_custo' adicionada com sucesso.")
        except OperationalError as e:
            print(f"Erro ao adicionar a coluna: {e}")
    else:
        print("A coluna 'codigo_centro_custo' já existe.")
