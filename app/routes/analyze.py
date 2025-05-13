from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.models.analyze import AnalyzeRequest, LLMResult, EntityEvidence
from app.services.file_service import load_selected_columns
from app.services.llm_input_builder import build_llm_input
from app.services.prompt_service import build_prompt_model_and_string
from app.services.llm_runner import run_entity_extraction

router = APIRouter()

@router.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        # 构建 Prompt 模型与 Prompt 模板
        model_class, prompt_class_str = build_prompt_model_and_string(
            [p.dict() for p in request.prompts]
        )

        # 读取 CSV 内容
        rows = load_selected_columns(request.csvFileName, request.selectedColumns)

        results = []
        for row in rows:
            article_input = build_llm_input(row, request.selectedColumns)
            llm_results = []

            for model in request.models:
                extracted = run_entity_extraction(prompt_class_str, model_class, article_input, model)
                structured = {
                    field: EntityEvidence(**value)
                    for field, value in extracted.items()
                    if isinstance(value, dict)
                }
                llm_results.append(LLMResult(model=model, extracted=structured))
             
            results.append({
                "id": row.get("__id__", ""),
                "columns": row,
                "llmResults": llm_results,
                "finalEntities": {}
            })

        return JSONResponse(content=jsonable_encoder({"results": results}))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
