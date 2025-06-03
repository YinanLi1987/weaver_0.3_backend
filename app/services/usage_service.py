#app/services/usage_service.py
from decimal import Decimal
from datetime import datetime
import uuid

from app.models.llm_usage_log import LLMUsageLog
from app.models.user import User
from sqlalchemy.orm import Session

PLATFORM_MARKUP = Decimal("1.3")  # 平台加价比例（30%）

def log_usage_and_charge_user(
    db: Session,
    user: User,
    model_id: str,
    input_tokens: int,
    output_tokens: int,
    base_cost: Decimal,
    prompt_summary: str = "",
):
    total_cost = base_cost * PLATFORM_MARKUP

    if user.balance < total_cost:
        raise ValueError("Insufficient balance. Task stopped early. Showing completed results.")

    usage_log = LLMUsageLog(
        id=str(uuid.uuid4()),
        user_id=user.uid,
        model=model_id,
        tokens_input=input_tokens,
        tokens_output=output_tokens,
        cost=base_cost,
        billed_amount=total_cost,
        prompt_summary=prompt_summary,
        timestamp=datetime.utcnow(),
    )

    db.add(usage_log)
    user.balance = Decimal(str(user.balance)) - total_cost
    db.commit()
    return usage_log
