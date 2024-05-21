from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import EmailStr, BaseModel
from .. import crud, schemas, databases
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

def send_reset_email(email: EmailStr):
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

@router.post("/api/send-reset-email/")
async def reset_password(email_request: EmailRequest, background_tasks: BackgroundTasks, db: Session = Depends(databases.get_db)):
    email = email_request.email
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email")

    background_tasks.add_task(send_reset_email, email)
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
    print('#################', users)
    return users
