#app/services/llm_runner.py
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
            
            result= run_gpt(prompt_class_str, model_schema, article_input, model)

        elif model.startswith("claude"):
            
            result=run_claude(prompt_class_str, model_schema, article_input, model)

        elif model.startswith("mistral"):
            
            result=run_mistral(prompt_class_str, model_schema, article_input, model)

        else:
            raise ValueError(f"Unsupported model: {model}")
        

        if not isinstance(result, dict):
            result = {"data": result}
        
        return {
            "data": result.get("data", result),  # 若直接返回 data 本体，也兼容
            "input_tokens": result.get("input_tokens", 0),
            "output_tokens": result.get("output_tokens", 0)
        }


    except Exception as e:
        print(f"❌ LLM extraction failed (model={model}):", e)
        #print(result)
        #print("🧵 Full prompt sent to model:")
        #print(full_prompt)
        print("🐛 Exception traceback:")
        traceback.print_exc()
        return {
             "data": {},
            "input_tokens": 0,
            "output_tokens": 0
        }
