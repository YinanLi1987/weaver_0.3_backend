from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from fastapi import BackgroundTasks
from app.services.redis_client import init_progress

from app.models.analyze import AnalyzeRequest, LLMResult, EntityEvidence
from app.services.file_service import load_selected_columns

from app.services.prompt_service import build_prompt_model_and_string

from app.services.tasks import run_analysis_task
import uuid

router = APIRouter()

@router.post("/analyze")
async def analyze(request: AnalyzeRequest,background_tasks: BackgroundTasks):
    try:
        task_id = str(uuid.uuid4())
        # 构建 Prompt 模型与 Prompt 模板
        model_class, prompt_class_str = build_prompt_model_and_string(
            [p.dict() for p in request.prompts]
        )

        # 读取 CSV 内容
        rows = load_selected_columns(request.csvFileName, request.selectedColumns)
        total_rows = len(rows)
         # Initialize Redis progress for this task
        init_progress(task_id, request.models, total_rows)
         # Run task in background
        background_tasks.add_task(
            run_analysis_task, task_id, request, model_class, prompt_class_str, rows
        )

        return JSONResponse(content={"taskId": task_id})

        
    except Exception as e:
        print(f"🔥 Analyze failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


