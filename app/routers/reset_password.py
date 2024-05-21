from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import EmailStr
from sqlalchemy.orm import Session
from .. import databases, utils, models

router = APIRouter(
    prefix="/api/reset_password",
    tags=["reset_password"],
)

@router.post("/")
async def reset_password(email: EmailStr, background_tasks: BackgroundTasks, db: Session = Depends(databases.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not registered",
        )
    background_tasks.add_task(utils.send_email_background, email=email)
    return {"message": "Password reset email sent"}
