import os
import uuid
import pandas as pd
from typing import List, Dict
from pathlib import Path

# Dynamic upload path (e.g. compatible with Heroku)
DEFAULT_DIR = "/tmp/uploads" if os.getenv("HEROKU") else "./uploads"
UPLOAD_DIR = Path(DEFAULT_DIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_upload_path(filename: str) -> Path:
    return UPLOAD_DIR / filename

async def save_upload_file(file) -> str:
    """
    Save uploaded file to UPLOAD_DIR with a unique UUID filename.
    """
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid.uuid4()}{ext}"
    filepath = get_upload_path(filename)

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    return filename

def extract_columns(filename: str) -> List[str]:
    """
    Read only the first row to extract column headers quickly.
    """
    filepath = get_upload_path(filename)
    df = pd.read_csv(filepath, nrows=1)
    return df.columns.tolist()

def load_selected_columns(filename: str, selected_columns: List[str]) -> List[Dict]:
    """
    Load selected columns from a CSV and add a string-based __id__ field.
    """
    filepath = get_upload_path(filename)
    df = pd.read_csv(filepath)
    df = df[selected_columns]
    df["__id__"] = df.index.astype(str)
    return df.to_dict(orient="records")
