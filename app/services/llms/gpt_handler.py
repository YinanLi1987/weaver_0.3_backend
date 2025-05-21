# services/llms/gpt_handler.py

from openai import OpenAI
from typing import List, Literal, Dict,Type
from instructor import from_openai
from pydantic import BaseModel
import tiktoken
from dotenv import load_dotenv
import os
if os.getenv("HEROKU") is None:
    
    load_dotenv(dotenv_path=".env")

def count_tokens(text: str, model: str) -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")  # fallback
    return len(encoding.encode(text))
def run_gpt(prompt_class_str: str, model_schema: type[BaseModel], article_input: str, model: str) -> Dict:
    system_prompt = (
        "You are an expert scientific information extractor. "
        "Use the following Pydantic BaseModel schema to extract structured data from the input."
    )
    full_prompt = f"{prompt_class_str}\n\nInput:\n{article_input}"
    input_tokens = count_tokens(system_prompt, model) + count_tokens(full_prompt, model)
    openai_client = from_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))
    try:
        

        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            response_model=model_schema,
            temperature=0.2,
            max_tokens=1024
        )
        
        output_text = str(response.dict())
        output_tokens = count_tokens(output_text, model)

        return {
            "data": response.dict(),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        }

    except Exception as e:
        print(f"❌ LLM extraction failed (model={model}):", e)
        return {
            "data": {},
            "input_tokens": input_tokens,
            "output_tokens": 0
        }