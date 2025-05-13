from typing import List, Callable, Dict, Any
from pydantic import BaseModel
from .llms.gpt_handler import run_gpt
from .llms.claude_handler import run_claude
from .llms.mistral_handler import run_mistral


def run_with_progress(
    rows: List[Dict[str, str]],
    models: List[str],
    prompt_class_str: str,
    model_schema: type[BaseModel],
    on_progress: Callable[[str, int, int], None] = None
) -> List[Dict[str, Any]]:
       
    progress = {model: 0 for model in models}
    total = len(rows)
    results = []

    for row in rows:
        row_result = {}
        for model in models:
            if model.startswith("gpt"):
                result = run_gpt(prompt_class_str, model_schema, row["text"], model)
            elif model.startswith("claude"):
                result = run_claude(prompt_class_str, model_schema, row["text"], model)
            elif model.startswith("mistral"):
                result = run_mistral(prompt_class_str, model_schema, row["text"], model)
            else:
                result = {}

            row_result[model] = result
            progress[model] += 1
            if on_progress:
                on_progress(model, progress[model], total)

        results.append(row_result)

    return results
