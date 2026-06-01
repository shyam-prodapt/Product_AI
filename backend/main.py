from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, analysis, chat, report
from config import settings
import os

app = FastAPI(title="Product Strategy AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.upload_dir, exist_ok=True)

app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(report.router, prefix="/api/report", tags=["Report"])

@app.get("/health")
def health():
    return {"status": "ok"}
