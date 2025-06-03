#app/routes/analyze_2.py
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user  
from app.services.redis_client import init_progress
from app.models.analyze import AnalyzeRequest
from app.services.file_service import load_selected_columns
from app.services.prompt_service import build_prompt_model_and_string
from app.services.task_service import run_analysis_task
import uuid
import asyncio
from fastapi import Request
router = APIRouter()
print("✅ analyze_2.py loaded!")

@router.post("/analyze")

async def analyze(
    #request: AnalyzeRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    print("🚀 Analyze called")
    body = await request.json()
    print("📥 Incoming /analyze payload:\n", body)
    print("🔧 DB session is:", db)
    print("👤 Current user is:", user.uid, user.email)


    try:
        parsed = AnalyzeRequest(**body)  # ✅ 触发 Pydantic 校验
    except Exception as e:
        print("❌ Validation error:", e)
        raise HTTPException(status_code=422, detail="Invalid AnalyzeRequest")


    try:
        
        task_id = str(uuid.uuid4())

        # Build prompt schema and string
        model_class, prompt_class_str = build_prompt_model_and_string(
            [p.dict() for p in parsed.prompts]
        )

        # Load data rows from uploaded CSV
        rows = load_selected_columns(parsed.csvFileName, parsed.selectedColumns)
        total_rows = len(rows)

        # Init Redis progress tracking
        init_progress(task_id, parsed.models, total_rows)

        # Run async analysis task in background
        asyncio.create_task(
    run_analysis_task(task_id, parsed, model_class, prompt_class_str, rows, db, user)
)

        return JSONResponse(content={"taskId": task_id})

    except Exception as e:
        print(f"🔥 Analyze failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
