# app/services/tasks.py
import json
import time
from fastapi.encoders import jsonable_encoder
from app.services.llm_input_builder import build_llm_input
from app.services.llm_runner import run_entity_extraction

from app.services.redis_client import increment_progress, r
from app.models.analyze import EntityEvidence, AnalyzeRequest, LLMResult

def run_analysis_task(task_id: str, request: AnalyzeRequest, model_class, prompt_class_str: str, rows: list[dict]):
    results = []
    # ✅ Initialize token counters
    total_input_tokens = 0
    total_output_tokens = 0
    # ✅ Per-model token counters
    model_token_stats = {
        model: {"input": 0, "output": 0} for model in request.models
    }
    model_time_stats = {model: 0.0 for model in request.models}

    for row in rows:
        article_input = build_llm_input(row, request.selectedColumns)
        llm_results = []

        for model in request.models:
            start_time = time.time()
            extracted = run_entity_extraction(prompt_class_str, model_class, article_input, model)
            elapsed = time.time() - start_time
            model_time_stats[model] += elapsed 
            # ✅ Accumulate tokens
            input_tokens = extracted.get("input_tokens", 0)
            output_tokens = extracted.get("output_tokens", 0)

            # ✅ Update per-model and total stats
            model_token_stats[model]["input"] += input_tokens
            model_token_stats[model]["output"] += output_tokens
            total_input_tokens += input_tokens
            total_output_tokens += output_tokens
            # Safely parse extracted results into structured format
            structured = {}
            for field, value in extracted.get("data", {}).items():
                if isinstance(value, dict) and "entities" in value and "evidence" in value:
                    try:
                        structured[field] = EntityEvidence(**value)
                    except Exception as e:
                        print(f"⚠️ Skipped invalid field '{field}': {e}")
                else:
                    print(f"⚠️ Skipped field '{field}': not a valid EntityEvidence object → {value}")

            llm_results.append(LLMResult(model=model, extracted=structured))
            increment_progress(task_id, model)

        results.append({
            "id": row.get("__id__", ""),
            "columns": row,
            "llmResults": llm_results,
            "finalEntities": {}
        })
    encoded_results = jsonable_encoder({"results": results})
     # ✅ Print detailed token stats
    print("📊 Token usage by model:")
    for model, stats in model_token_stats.items():
        print(f"- {model}: input={stats['input']}, output={stats['output']}")
    print("⏱️  Time spent by model:")
    for model, seconds in model_time_stats.items():
        print(f"- {model}: {seconds:.2f} seconds")
    print(f"📊 Total input tokens: {total_input_tokens}")
    print(f"🧾 Total output tokens: {total_output_tokens}")
    r.set(f"analyze_results:{task_id}", json.dumps(encoded_results), ex=3600)
    print(f"✅ Background task {task_id} finished.")
