from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.redis_client import get_progress

router = APIRouter()

@router.get("/progress/{task_id}")
async def progress(task_id: str):
    """Expose task progress by task ID."""
    data = get_progress(task_id)
    if not data:
        raise HTTPException(status_code=404, detail="Progress not found")
    return JSONResponse(content=data)
