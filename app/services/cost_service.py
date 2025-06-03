from decimal import Decimal
from app.models.llm_model import LLMModel

def calculate_cost(db, model_id: str, input_tokens: int, output_tokens: int) -> Decimal:
    model = db.query(LLMModel).filter(LLMModel.id == model_id).first()
    if not model:
        raise ValueError(f"Model {model_id} not found")

    return (
        Decimal(input_tokens) * model.input_cost_per_1k +
        Decimal(output_tokens) * model.output_cost_per_1k
    ) / Decimal(1000)
