from fastapi import APIRouter, UploadFile, File, Form
from typing import List
import uuid
import os
import shutil
from config import settings
from services.file_parser import process_files
from services.pinecone_service import get_pinecone_service
from models.schemas import UploadResponse

router = APIRouter()

@router.post("/", response_model=UploadResponse)
async def upload_files(
    files: List[UploadFile] = File(...),
    session_id: str = Form(default=None),
):
    if not session_id:
        session_id = str(uuid.uuid4())
    session_dir = os.path.join(settings.upload_dir, session_id)
    os.makedirs(session_dir, exist_ok=True)
    file_paths = []
    for file in files:
        filepath = os.path.join(session_dir, file.filename)
        with open(filepath, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_paths.append(filepath)
    chunks = await process_files(file_paths, session_id)
    await get_pinecone_service().upsert_chunks(session_id, chunks)
    return UploadResponse(
        session_id=session_id,
        files_processed=len(file_paths),
        chunks_indexed=len(chunks),
        message=f"Processed {len(files)} file(s) and indexed {len(chunks)} chunks.",
    )
