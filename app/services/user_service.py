from sqlalchemy.orm import Session
from app.models.user import User
from app.db import SessionLocal

def get_or_create_user(uid: str, email: str) -> User:
    db: Session = SessionLocal()
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        user = User(uid=uid, email=email, balance=0.0)
        db.add(user)
        db.commit()
        db.refresh(user)
    db.close()
    return user

def update_user_balance(uid: str, amount: float):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.uid == uid).first()
    if user:
        user.balance += amount
        db.commit()
    db.close()
