from mistralai import Mistral
from instructor import from_mistral, Mode
from typing import List, Literal, Dict,Type
from pydantic import BaseModel
from dotenv import load_dotenv
import os

if os.getenv("HEROKU") is None:
    load_dotenv(dotenv_path=".env")



# Estimated token count for Mistral: 1 token ≈ 4 characters
def count_tokens_mistral(text: str) -> int:
    return max(1, len(text) // 4)
def run_mistral(prompt_class_str: str, model_schema: type[BaseModel], article_input: str, model: str) -> Dict:
    system_prompt = (
        "You are an expert scientific information extractor. "
        "Use the following Pydantic BaseModel schema to extract structured data from the input."
    )
    full_prompt = f"{prompt_class_str}\n\nInput:\n{article_input}"
    input_tokens = count_tokens_mistral(full_prompt)

    try:
        client = from_mistral(
            client=Mistral(api_key=os.getenv("MISTRALAI_API_KEY")),
            mode=Mode.MISTRAL_TOOLS  # 用老接口
        )

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

        output_text = str(response.dict())
        output_tokens = count_tokens_mistral(output_text)

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
