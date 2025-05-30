# app/models/payment_log.py
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from datetime import datetime
from app.db import Base
from decimal import Decimal
from sqlalchemy.orm import relationship
import uuid
class PaymentLog(Base):
    __tablename__ = "payment_logs"

    id = Column(String, primary_key=True, index=True,default=lambda: str(uuid.uuid4()))  # 可用 Stripe session_id
    user_id = Column(String, ForeignKey("users.uid"), nullable=False)
    amount = Column(Numeric(20, 6), nullable=False)
    currency = Column(String(10), default="eur", nullable=False)
    stripe_session_id = Column(String, nullable=False)
    #status = Column(String, default="success")  # success / failed / refunded
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="payment_logs")
