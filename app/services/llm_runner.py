from pydantic import BaseModel
from typing import Dict
import traceback
from .llms.mistral_handler import run_mistral
from .llms.gpt_handler import run_gpt
from .llms.claude_handler import run_claude

def run_entity_extraction(prompt_class_str: str, model_schema: type[BaseModel], article_input: str, model: str) -> Dict:
    #full_prompt = f"{prompt_class_str}\n\nInput:\n{article_input}"
    print(f"✅ Calling model: {model}")

    try:
        if model.startswith("gpt"):
            
            return run_gpt(prompt_class_str, model_schema, article_input, model)

        elif model.startswith("claude"):
            
            return run_claude(prompt_class_str, model_schema, article_input, model)

        elif model.startswith("mistral"):
            
            return run_mistral(prompt_class_str, model_schema, article_input, model)

        else:
            raise ValueError(f"Unsupported model: {model}")

    except Exception as e:
        print(f"❌ LLM extraction failed (model={model}):", e)
        #print("🧵 Full prompt sent to model:")
        #print(full_prompt)
        print("🐛 Exception traceback:")
        traceback.print_exc()
        return {}
