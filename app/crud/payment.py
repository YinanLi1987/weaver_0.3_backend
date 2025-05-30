# app/crud/payment.py

from sqlalchemy.orm import Session
from app.models.payment_log import PaymentLog
from decimal import Decimal
from datetime import datetime
from typing import Optional

def log_payment(
    db: Session,
    user_id: str,
    amount: Decimal,
    stripe_session_id: str,
    currency: str = "eur",
    timestamp: Optional[datetime] = None,
    
) -> PaymentLog:
 
   
    if amount <= Decimal("0.00"):
        raise ValueError("Amount must be positive")
    existing = db.query(PaymentLog).filter_by(stripe_session_id=stripe_session_id).first()
    if existing:
        raise ValueError("This Stripe session was already logged")
    payment = PaymentLog(
        user_id=user_id,
        amount=amount,
        stripe_session_id=stripe_session_id,
        currency=currency,
        timestamp=timestamp or datetime.utcnow()
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
def get_payments_for_user(db: Session, user_id: str):
    return (
        db.query(PaymentLog)
        .filter(PaymentLog.user_id == user_id)
        .order_by(PaymentLog.timestamp.desc())
        .all()
    )
