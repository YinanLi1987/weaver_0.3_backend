# app/routes/user_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.firebase_auth import verify_firebase_token
from app.crud.user import get_or_create_user

router = APIRouter()


@router.get("/me")
def get_user_info(
    uid_email=Depends(verify_firebase_token),
    db: Session = Depends(get_db)
):
    uid, email = uid_email
    user = get_or_create_user(db, user_id=uid, email=email)

    return {
        "uid": user.uid,
        "email": user.email,
        "balance": round(user.balance, 4)
    }
