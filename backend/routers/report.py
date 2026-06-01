from fastapi import APIRouter
from fastapi.responses import Response
from models.schemas import AnalysisResponse
from services.pdf_generator import generate_pdf_report

router = APIRouter()

@router.post("/download")
async def download_report(analysis: AnalysisResponse):
    pdf_bytes = generate_pdf_report(analysis)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=product-strategy-report.pdf"
        },
    )
