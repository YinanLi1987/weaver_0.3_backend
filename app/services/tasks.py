# app/services/tasks.py
import json
from fastapi.encoders import jsonable_encoder
from app.services.llm_input_builder import build_llm_input
from app.services.llm_runner import run_entity_extraction

from app.services.redis_client import increment_progress, r
from app.models.analyze import EntityEvidence, AnalyzeRequest, LLMResult

def run_analysis_task(task_id: str, request: AnalyzeRequest, model_class, prompt_class_str: str, rows: list[dict]):
    results = []

    for row in rows:
        article_input = build_llm_input(row, request.selectedColumns)
        llm_results = []

        for model in request.models:
            extracted = run_entity_extraction(prompt_class_str, model_class, article_input, model)
            structured = {
                field: EntityEvidence(**value)
                for field, value in extracted.items()
                if isinstance(value, dict)
            }
            llm_results.append(LLMResult(model=model, extracted=structured))
            increment_progress(task_id, model)

        results.append({
            "id": row.get("__id__", ""),
            "columns": row,
            "llmResults": llm_results,
            "finalEntities": {}
        })
    encoded_results = jsonable_encoder({"results": results})
    r.set(f"analyze_results:{task_id}", json.dumps(encoded_results), ex=3600)
    print(f"✅ Background task {task_id} finished.")
