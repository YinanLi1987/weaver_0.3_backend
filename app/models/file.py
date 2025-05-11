from pydantic import BaseModel
from typing import List

class UploadCSVResponse(BaseModel):
    filename: str
    columns: List[str]
