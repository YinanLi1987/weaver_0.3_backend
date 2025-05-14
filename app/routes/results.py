from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.redis_client import r
import json
router = APIRouter()

@router.get("/results/{task_id}")
async def get_results(task_id: str):
    raw = r.get(f"analyze_results:{task_id}")
    if raw is None:
        raise HTTPException(status_code=404, detail="Result not ready or expired")
    return JSONResponse(content=json.loads(raw))
