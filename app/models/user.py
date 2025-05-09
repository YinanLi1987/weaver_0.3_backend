from sqlalchemy import Column, String, Float
from app.db import Base

class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.0)
