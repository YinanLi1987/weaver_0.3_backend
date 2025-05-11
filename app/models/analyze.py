from pydantic import BaseModel
from typing import List, Dict,Optional
from app.models.prompt import PromptDefinition

class AnalyzeRequest(BaseModel):
    prompts: List[PromptDefinition]
    models: List[str]
    csvFileName: Optional[str] = None
    selectedColumns: Optional[List[str]] = None
    rows: Optional[List[Dict[str, str]]] = None 

class EntityEvidence(BaseModel):
    entities: List[str]
    evidence: List[str]

class LLMResult(BaseModel):
    model: str
    extracted: Dict[str, EntityEvidence]


class AnalyzeResultItem(BaseModel):
    id: str
    columns: Dict[str, str]  # dynamically selected user fields
    llmResults: List[LLMResult]
    finalEntities: Dict[str, List[str]]