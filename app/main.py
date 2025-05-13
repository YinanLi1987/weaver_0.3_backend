import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from dotenv import load_dotenv
load_dotenv()
from app.routes.user_routes import router as user_router  # ✅ 更干净地导入 router
from app.routes.stripe_routes import router as stripe_router
from app.routes import stripe_webhook
from app.routes import upload
from app.routes import analyze
from app.routes import progress

app = FastAPI()
# Allow frontend dev server to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev server origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Optional test route
@app.get("/api/hello")
def read_root():
    return {"message": "Hello from FastAPI!"}

# Include user API routes
app.include_router(user_router)
app.include_router(stripe_router)
app.include_router(stripe_webhook.router)
app.include_router(upload.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")
app.include_router(progress.router,prefix="/api")