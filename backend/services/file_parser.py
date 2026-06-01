from typing import List, Dict, Any
from pathlib import Path

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return [c for c in chunks if len(c.strip()) > 50]

def parse_pdf(filepath: str) -> str:
    import PyPDF2
    text = ""
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def parse_docx(filepath: str) -> str:
    from docx import Document
    doc = Document(filepath)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def parse_csv(filepath: str) -> str:
    import pandas as pd
    df = pd.read_csv(filepath)
    summary = f"Dataset: {len(df)} rows, {len(df.columns)} columns\n"
    summary += f"Columns: {', '.join(df.columns.tolist())}\n\n"
    summary += "Summary Statistics:\n"
    try:
        summary += df.describe().to_string() + "\n\n"
    except Exception:
        pass
    summary += "Full Data Sample (first 50 rows):\n"
    summary += df.head(50).to_string()
    if len(df) > 50:
        summary += f"\n\n... ({len(df) - 50} more rows)\n"
        summary += df.tail(20).to_string()
    return summary

def parse_txt(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def parse_file(filepath: str) -> str:
    ext = Path(filepath).suffix.lower()
    parsers = {
        ".pdf": parse_pdf,
        ".docx": parse_docx,
        ".csv": parse_csv,
        ".txt": parse_txt,
        ".md": parse_txt,
    }
    return parsers.get(ext, parse_txt)(filepath)

async def process_files(file_paths: List[str], session_id: str) -> List[Dict[str, Any]]:
    from services.embedding_service import get_embeddings_batch

    all_chunks = []
    chunk_counter = 0
    for filepath in file_paths:
        text = parse_file(filepath)
        chunks = chunk_text(text)
        source = Path(filepath).name
        for chunk in chunks:
            all_chunks.append(
                {"chunk_id": str(chunk_counter), "text": chunk, "source": source}
            )
            chunk_counter += 1
    texts = [c["text"] for c in all_chunks]
    embeddings = await get_embeddings_batch(texts)
    for i, chunk in enumerate(all_chunks):
        chunk["embedding"] = embeddings[i]
    return all_chunks
