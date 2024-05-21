from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
import aiosqlite
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

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

# Modelo de dados do usuário
class User(BaseModel):
    username: str
    email: EmailStr

# Modelo de criação de usuário
class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str

# Modelo de autenticação
class Token(BaseModel):
    access_token: str
    token_type: str

# Função para obter a conexão do banco de dados
async def get_db():
    db = await aiosqlite.connect("test.db")
    try:
        yield db
    finally:
        await db.close()

# Inicialização do banco de dados
@app.on_event("startup")
async def startup():
    async with aiosqlite.connect("test.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)
        await db.commit()

# Configurações de segurança
SECRET_KEY = "a_very_secret_key"  # Altere isso para uma chave secreta forte
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Função para verificar a senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar o hash da senha
def get_password_hash(password):
    return pwd_context.hash(password)

# Função para criar o token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para enviar e-mail em segundo plano
def send_email_background(email: str):
    corpo_email = """\
    Clique no link para redefinir sua senha: <link>
    <p>Parágrafo1</p>
    <p>Parágrafo2</p>
    """

    sender_email = os.environ["EMAIL_USER"]
    sender_password = os.environ["EMAIL_PASS"]
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Redefinição de senha"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Clique no link para redefinir sua senha: <link>
    """
    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

# Rota para verificar o usuário e enviar e-mail de redefinição de senha
@app.post("/api/send-reset-email/")
async def send_reset_email(user: User, background_tasks: BackgroundTasks, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM users WHERE username = ? AND email = ?", (user.username, user.email))
    user_db = await cursor.fetchone()
    if not user_db:
        raise HTTPException(status_code=400, detail="Login ou e-mail inválido.")

    # Adiciona a tarefa de envio de e-mail ao fundo
    background_tasks.add_task(send_email_background, user.email)

    return {"message": "E-mail de redefinição de senha enviado com sucesso."}

# Rota para criar novo usuário
@app.post("/api/create-user/")
async def create_user(new_user: CreateUser, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM users WHERE username = ? OR email = ?", (new_user.username, new_user.email))
    existing_user = await cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário ou e-mail já existe.")

    hashed_password = get_password_hash(new_user.password)
    await db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (new_user.username, new_user.email, hashed_password))
    await db.commit()
    return {"message": "Usuário criado com sucesso."}

# Rota para autenticação de login
@app.post("/api/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM users WHERE username = ?", (form_data.username,))
    user_db = await cursor.fetchone()
    if not user_db or not verify_password(form_data.password, user_db[3]):
        raise HTTPException(
            status_code=400,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_db[1]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Rota para listar todos os usuários
@app.get("/api/users/")
async def read_users(db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT id, username, email, password FROM users")
    users = await cursor.fetchall()
    print('##############', users)
    return [{"id": row[0], "username": row[1], "email": row[2], "password": row[3]} for row in users]
