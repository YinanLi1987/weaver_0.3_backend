# app/firebase_auth.py
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from fastapi import Header, HTTPException, status

# Initialize Firebase Admin SDK only once
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

def verify_firebase_token(authorization: str = Header(...)) -> tuple[str, str]:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.split("Bearer ")[1]
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        uid = decoded_token["uid"]
        email = decoded_token.get("email", "")
        return uid, email
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
