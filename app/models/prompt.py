from pydantic import BaseModel
from typing import List

class PromptDefinition(BaseModel):
    name: str
    description: str
    examples: List[str]
