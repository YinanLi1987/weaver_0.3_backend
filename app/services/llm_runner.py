import os
import instructor
from openai import OpenAI 
from anthropic import Anthropic
from mistralai.client import MistralClient

from pydantic import BaseModel, Field
from typing import List, Literal, Dict
from dotenv import load_dotenv
import os

if os.getenv("HEROKU") is None:
    
    load_dotenv(dotenv_path=".env")
    #print("KEY:", os.getenv("MISTRALAI_API_KEY"))


def get_instructor_client(model: str):
    """
    Select the correct instructor client based on the model prefix.
    Each LLM provider uses its own client and API key.
    """
    if model.startswith("gpt"):
        return instructor.from_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))
    elif model.startswith("claude"):
        return instructor.from_anthropic(Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")))
    elif model.startswith("mistral"):
        return instructor.from_mistral(MistralClient(api_key=os.getenv("MISTRALAI_API_KEY")))
    else:
        raise ValueError(f"Unsupported model: {model}")

def run_entity_extraction(prompt_class_str: str, model_schema: type[BaseModel], article_input: str, model: str) -> Dict:
    """
    使用 instructor + 多个 LLM 模型提取结构化实体
    """
    system_prompt = (
        "You are an expert scientific information extractor. "
        "Use the following Pydantic BaseModel schema to extract structured data from the input."
    )

    full_prompt = f"{prompt_class_str}\n\nInput:\n{article_input}"
    print("Full prompt:", full_prompt)

    try:
        client = get_instructor_client(model)

        response = client.chat.completions.create(
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
