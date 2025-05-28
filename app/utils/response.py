import math
from fastapi.responses import JSONResponse

def clean_nan(obj):
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    elif isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan(i) for i in obj]
    return obj

def safe_json_response(data, status_code=200):
    """
    自动清洗数据中的 NaN/Infinity 并安全返回 JSONResponse
    """
    try:
        cleaned = clean_nan(data)
        return JSONResponse(content=cleaned, status_code=status_code)
    except Exception as e:
        return JSONResponse(
            content={"error": "Failed to serialize response", "detail": str(e)},
            status_code=500
        )
