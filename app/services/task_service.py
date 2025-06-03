#app/services/task_service.py
import json
import time
import asyncio
from decimal import Decimal
from fastapi.encoders import jsonable_encoder
from app.services.llm_input_builder import build_llm_input
from app.services.llm_runner import run_entity_extraction
from app.services.redis_client import increment_progress, r
from app.models.analyze import EntityEvidence, AnalyzeRequest, LLMResult
from app.services.cost_service import calculate_cost
from app.services.usage_service import log_usage_and_charge_user
from sqlalchemy.orm import Session


async def process_model_for_row(db, user, task_id, row_id, model, article_input, model_class, prompt_class_str, results):
    try:
        user = db.merge(user)
        start_time = time.time()
        extracted = await run_entity_extraction(prompt_class_str, model_class, article_input, model)
        elapsed = time.time() - start_time

        input_tokens = extracted.get("input_tokens", 0)
        output_tokens = extracted.get("output_tokens", 0)

        base_cost = calculate_cost(db, model, input_tokens, output_tokens)

        log_usage_and_charge_user(
            db=db,
            user=user,
            model_id=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            base_cost=base_cost,
            prompt_summary=article_input[:100]
        )

        structured = {}
        for field, value in extracted.get("data", {}).items():
            if isinstance(value, dict) and "entities" in value and "evidence" in value:
                try:
                    structured[field] = EntityEvidence(**value)
                except Exception as e:
                    print(f"⚠️ Invalid field '{field}': {e}")

        result = {
            "model": model,
            "extracted": structured,
            "duration": elapsed
        }
        increment_progress(task_id, model)
        return result

    except ValueError as e:
        if "Insufficient balance" in str(e):
            print(f"🛑 Balance insufficient for model {model}, task stopped.")
            raise e
        else:
            print(f"❌ Error processing model {model}: {e}")
            return None

async def run_analysis_task(task_id: str, request: AnalyzeRequest, model_class, prompt_class_str: str, rows: list[dict], db, user):
    results = []

    try:
        for row in rows:
            article_input = build_llm_input(row, request.selectedColumns)
            tasks = [
                process_model_for_row(
                    db, user, task_id, row.get("__id__", ""),
                    model, article_input, model_class, prompt_class_str, results
                )
                for model in request.models
            ]

            try:
                model_results = await asyncio.gather(*tasks, return_exceptions=True)
            except ValueError as e:
                if "Insufficient balance" in str(e):
                    partial = jsonable_encoder({
                        "status": "partial",
                        "message": str(e),
                        "results": results
                    })
                    r.set(f"analyze_results:{task_id}", json.dumps(partial), ex=3600)
                    print(f"⚠️ Task {task_id} ended early due to insufficient balance.")
                    return

            llm_results = [
                LLMResult(model=result["model"], extracted=result["extracted"])
                for result in model_results if result
            ]

            results.append({
                "id": row.get("__id__", ""),
                "columns": row,
                "llmResults": llm_results,
                "finalEntities": {}
            })

        # ✅ 全部成功，写入 completed
        encoded_results = jsonable_encoder({"status": "completed", "results": results})
        r.set(f"analyze_results:{task_id}", json.dumps(encoded_results), ex=3600)
        print(f"✅ Task {task_id} completed.")

    except Exception as e:
        import traceback
        print(f"🔥 Unexpected error in task {task_id}: {e}")
        traceback.print_exc()

        error_result = jsonable_encoder({
            "status": "error",
            "message": str(e),
            "results": results  # ✅ 即使 error，也保留已完成部分
        })
        r.set(f"analyze_results:{task_id}", json.dumps(error_result), ex=3600)