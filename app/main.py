from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, auth, reset_password
from app.databases import Base, engine
import os
from dotenv import load_dotenv

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # Adicione o endereço do seu frontend aqui
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(reset_password.router)
