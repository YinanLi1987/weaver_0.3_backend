from sqlalchemy import Column, String, Float,DateTime
from datetime import datetime
from app.db import Base

class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    stripe_customer_id = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
