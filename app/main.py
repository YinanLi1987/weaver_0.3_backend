import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from app.models import user, llm_usage_log, payment_log
from dotenv import load_dotenv
load_dotenv()
from app.routes import user_routes
from app.routes import stripe_routes
from app.routes import stripe_webhook
from app.routes import upload
from app.routes import analyze
from app.routes import progress
from app.routes import results
#Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost:5173",  # 本地开发
    "http://localhost:3000",  # serve dist 本地测试
    "https://weaver-03.vercel.app" ,
    "https://weaver-03-yinanli1987s-projects.vercel.app/"# 生产站点
]
# Allow frontend dev server to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Frontend dev server origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Optional test route
@app.get("/api/hello")
def read_root():
    return {"message": "Hello from FastAPI!"}

# Include user API routes
app.include_router(user_routes.router,prefix="/api/user")
app.include_router(stripe_routes.router,prefix="/api/stripe")
app.include_router(stripe_webhook.router,prefix="/api/stripe")
app.include_router(upload.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")
app.include_router(progress.router, prefix="/api")
app.include_router(results.router, prefix="/api")