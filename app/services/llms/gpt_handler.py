# services/llms/gpt_handler.py

from openai import OpenAI
from typing import List, Literal, Dict
from instructor import from_openai
from pydantic import BaseModel
from dotenv import load_dotenv
import os
if os.getenv("HEROKU") is None:
    
    load_dotenv(dotenv_path=".env")


def run_gpt(prompt_class_str: str, model_schema: type[BaseModel], article_input: str, model: str) -> Dict:
    system_prompt = (
        "You are an expert scientific information extractor. "
        "Use the following Pydantic BaseModel schema to extract structured data from the input."
    )
    full_prompt = f"{prompt_class_str}\n\nInput:\n{article_input}"
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
        return response.dict()

    except Exception as e:
        print(f"❌ LLM extraction failed (model={model}):", e)
        return {}