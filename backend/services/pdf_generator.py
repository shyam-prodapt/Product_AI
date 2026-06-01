from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable,
)
from reportlab.lib.enums import TA_CENTER
import io
from models.schemas import AnalysisResponse
from datetime import datetime

PRIMARY = colors.HexColor("#1a1a2e")
ACCENT = colors.HexColor("#e94560")
BLUE = colors.HexColor("#0f3460")
LIGHT_BG = colors.HexColor("#f8f9fa")


def generate_pdf_report(analysis: AnalysisResponse) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        spaceAfter=10,
        textColor=PRIMARY,
        alignment=TA_CENTER,
    )
    h1 = ParagraphStyle(
        "H1", parent=styles["Heading1"], fontSize=15, spaceBefore=18, spaceAfter=8, textColor=PRIMARY
    )
    h2 = ParagraphStyle(
        "H2", parent=styles["Heading2"], fontSize=12, spaceBefore=12, spaceAfter=5, textColor=BLUE
    )
    body = ParagraphStyle(
        "Body", parent=styles["Normal"], fontSize=9.5, spaceAfter=5, leading=15
    )
    story = []

    # Cover
    story.append(Spacer(1, 0.8 * inch))
    story.append(Paragraph("AI Product Strategy Report", title_style))
    story.append(
        Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}", body)
    )
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT))
    story.append(Spacer(1, 0.4 * inch))

    # Executive Summary
    story.append(Paragraph("Executive Summary", h1))
    story.append(
        Paragraph(analysis.executive_summary or "No executive summary generated.", body)
    )
    story.append(PageBreak())

    # SWOT
    story.append(Paragraph("SWOT Analysis", h1))
    swot = analysis.swot or {}

    def bullets(lst):
        return "\n".join([f"• {x}" for x in (lst or [])[:5]])

    swot_data = [
        ["STRENGTHS", "WEAKNESSES"],
        [bullets(swot.get("strengths", [])), bullets(swot.get("weaknesses", []))],
        ["OPPORTUNITIES", "THREATS"],
        [bullets(swot.get("opportunities", [])), bullets(swot.get("threats", []))],
    ]
    swot_table = Table(swot_data, colWidths=[3.2 * inch, 3.2 * inch])
    swot_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#d4edda")),
                ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#f8d7da")),
                ("BACKGROUND", (0, 2), (0, 2), colors.HexColor("#cce5ff")),
                ("BACKGROUND", (1, 2), (1, 2), colors.HexColor("#fff3cd")),
                ("FONTNAME", (0, 0), (1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 2), (1, 2), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(swot_table)
    story.append(Spacer(1, 0.3 * inch))

    # Insights
    story.append(Paragraph("Strategic Insights", h1))
    for i, insight in enumerate((analysis.insights or [])[:10], 1):
        story.append(Paragraph(f"{i}. {insight}", body))
    story.append(PageBreak())

    # Feature Prioritization
    story.append(Paragraph("Feature Prioritization", h1))
    features = analysis.feature_priorities or []
    if features:
        feat_data = [["Feature", "Impact", "Effort", "Priority"]]
        for f in features[:10]:
            feat_data.append(
                [
                    f.get("name", "N/A"),
                    str(f.get("impact", "-")),
                    str(f.get("effort", "-")),
                    str(round(float(f.get("priority_score", 0)), 2)),
                ]
            )
        ft = Table(feat_data, colWidths=[3.2 * inch, 0.9 * inch, 0.9 * inch, 1.1 * inch])
        ft.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(ft)

    # Opportunities
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Product Opportunities", h1))
    for opp in (analysis.opportunities or [])[:6]:
        story.append(
            Paragraph(
                f"<b>{opp.get('title', 'Opportunity')}</b> — Score: {opp.get('score', 'N/A')}/10",
                h2,
            )
        )
        story.append(Paragraph(opp.get("description", ""), body))

    # Roadmap
    story.append(PageBreak())
    story.append(Paragraph("Product Roadmap", h1))
    for phase in (analysis.roadmap or [])[:4]:
        story.append(Paragraph(phase.get("quarter", "Phase"), h2))
        story.append(Paragraph(f"Theme: {phase.get('theme', '')}", body))
        for feat in phase.get("features", []):
            story.append(Paragraph(f"  • {feat}", body))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
