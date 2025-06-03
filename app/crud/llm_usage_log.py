# app/crud/usage.py

from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.llm_usage_log import LLMUsageLog

def get_usage_logs_for_user(db: Session, user_id: str, limit: int = 100):
    return (
        db.query(LLMUsageLog)
        .filter(LLMUsageLog.user_id == user_id)
        .order_by(desc(LLMUsageLog.timestamp))
        .limit(limit)
        .all()
    )
