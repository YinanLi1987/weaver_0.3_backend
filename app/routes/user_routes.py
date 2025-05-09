from fastapi import APIRouter, Depends
from app.firebase_auth import verify_firebase_token

router = APIRouter(prefix="/api/user")

@router.get("/me")
def get_user_info(uid_email=Depends(verify_firebase_token)):
    # Unpack UID and email from Firebase token
    uid, email = uid_email
    # For now, return a placeholder response
    return {
        "uid": uid,
        "email": email,
        "balance": 0.00  # 占位数据
    }
