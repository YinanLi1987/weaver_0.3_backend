#app/routes/upload.py
from fastapi import APIRouter, UploadFile, File
from app.services.file_service import save_upload_file, extract_columns
from app.models.file import UploadCSVResponse

router = APIRouter()

@router.post("/upload_csv", response_model=UploadCSVResponse)
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload a CSV file, save it to server, and return available columns.
    """
    filename = await save_upload_file(file)
    columns = extract_columns(filename)
    return UploadCSVResponse(filename=filename, columns=columns)
