from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import EmailStr, BaseModel, Field
from app import crud, schemas, databases
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import aiosqlite

load_dotenv()

router = APIRouter()

class EmailRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
RESET_PASSWORD_TOKEN_EXPIRE_HOURS = 1

def send_reset_email(email: EmailStr, token: str):
    sender_email = os.environ["EMAIL_USER"]
    sender_password = os.environ["EMAIL_PASS"]
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Redefinição de senha"
    message["From"] = sender_email
    message["To"] = receiver_email

    # text = """\
    # Clique no link para redefinir sua senha: <link>
    # """
    reset_link = f"http://localhost:3000/auth/new-password?token={token}"
    text = f"Clique no link para redefinir sua senha: {reset_link}"
    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
def create_reset_password_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=RESET_PASSWORD_TOKEN_EXPIRE_HOURS)
    to_encode = {"exp": expire, "email": email}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_reset_password_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = decoded_token.get("email")
        return email
    except JWTError:
        return None
    
@router.post("/api/send-reset-email/")
async def reset_password(email_request: EmailRequest, background_tasks: BackgroundTasks, db: Session = Depends(databases.get_db)):
    email = email_request.email
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email")

    reset_token = create_reset_password_token(email)
    background_tasks.add_task(send_reset_email, email, reset_token)
    return {"message": "Password reset email sent"}

@router.post("/api/create-user/", response_model=schemas.User)
async def create_user(user: schemas.CreateUser, db: Session = Depends(databases.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/api/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(databases.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/api/users/all", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(databases.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/api/reset-password/")
async def reset_password(reset_request: ResetPasswordRequest, db: Session = Depends(databases.get_db)):
    email = verify_reset_password_token(reset_request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")

    hashed_password = pwd_context.hash(reset_request.new_password)
    user.password = hashed_password
    db.commit()

    return {"message": "Password updated successfully"}