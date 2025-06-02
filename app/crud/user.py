# app/crud/user.py

from sqlalchemy.orm import Session
from app.models.user import User
from typing import Optional
from decimal import Decimal


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.uid == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_stripe_customer_id(db: Session, customer_id: str) -> Optional[User]:
    return db.query(User).filter(User.stripe_customer_id == customer_id).first()


def create_user(db: Session, user_id: str, email: str) -> User:
    user = User(uid=user_id, email=email, balance=0.0)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_user(db: Session, user_id: str, email: str) -> User:
    user = get_user_by_id(db, user_id)
    if user:
        return user
    return create_user(db, user_id, email)


def update_user_balance(db: Session, user_id: str, delta: Decimal) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")

    new_balance = Decimal(user.balance or 0) + delta

    if new_balance < 0:
        raise ValueError("Insufficient balance")

    user.balance = new_balance
    db.commit()
    db.refresh(user)
    return user
def deduct_user_credits(db: Session, user_id: str, cost: float) -> User:
     if cost <= 0:
        raise ValueError("Cost must be positive")
     return update_user_balance(db, user_id=user_id, delta=-cost)