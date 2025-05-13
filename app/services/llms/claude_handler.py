from anthropic import Anthropic
from instructor import from_anthropic
from pydantic import BaseModel
from dotenv import load_dotenv
import os

if os.getenv("HEROKU") is None:
    load_dotenv(dotenv_path=".env")


def run_claude(prompt_class_str: str, model_schema: type[BaseModel], article_input: str, model: str) -> dict:
    system_prompt = (
        "You are an expert scientific information extractor. "
        "Use the following Pydantic BaseModel schema to extract structured data from the input."
    )
    full_prompt = f"{prompt_class_str}\n\nInput:\n{article_input}"

    try:
        client = from_anthropic(Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")))

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
