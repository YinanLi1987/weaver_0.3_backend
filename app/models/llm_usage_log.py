# app/models/llm_usage_log.py
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from app.db import Base

class LLMUsageLog(Base):
    __tablename__ = "llm_usage_logs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.uid"), nullable=False)
    model = Column(String, nullable=False)
    tokens_input = Column(Integer, default=0)
    tokens_output = Column(Integer, default=0)
    cost = Column(Float, nullable=False)  
    timestamp = Column(DateTime, default=datetime.utcnow)
    prompt_summary = Column(String, nullable=True)
