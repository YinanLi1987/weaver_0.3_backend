#app/models/llm_model.py
from sqlalchemy import Column, String, Numeric
from app.db import Base

class LLMModel(Base):
    __tablename__ = "llm_models"

    id = Column(String, primary_key=True)  # e.g. gpt-4.1-nano
    name = Column(String, nullable=False)  # e.g. GPT-4
    input_cost_per_1k = Column(Numeric(precision=10, scale=6))  # 最多 6 位小数
    output_cost_per_1k = Column(Numeric(precision=10, scale=6))
