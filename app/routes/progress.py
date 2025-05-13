# backend/api/progress.py

from fastapi import APIRouter
from app.state import progress_tracker, progress_total_rows # a global dict per model

router = APIRouter()

@router.get("/progress")
def get_progress():
      return {
        "progress": progress_tracker,        # e.g. {"gpt-4": 22, ...}
        "total": progress_total_rows         # e.g. 100
    } # e.g., {"gpt-4": 42, "mistral": 17}
