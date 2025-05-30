# app/models/payment_log.py
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.db import Base

class PaymentLog(Base):
    __tablename__ = "payment_logs"

    id = Column(String, primary_key=True, index=True)  # 可用 Stripe session_id
    user_id = Column(String, ForeignKey("users.uid"), nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String, default="stripe")
    stripe_session_id = Column(String, nullable=False)
    status = Column(String, default="success")  # success / failed / refunded
    timestamp = Column(DateTime, default=datetime.utcnow)
