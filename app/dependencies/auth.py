# app/dependencies/auth.py
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.firebase_auth import verify_firebase_token
from app.models.user import User

def get_current_user(
    db: Session = Depends(get_db),
    token_data: tuple[str, str] = Depends(verify_firebase_token)
) -> User:
    uid, email = token_data
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        raise Exception("User not found in database")
    return user
