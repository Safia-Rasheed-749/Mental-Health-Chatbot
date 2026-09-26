"""Generate a privacy-conscious wellness summary PDF for a user."""

from __future__ import annotations

from datetime import datetime
from io import BytesIO


def build_wellness_pdf(username: str, moods: list, journals: list, message_count: int) -> bytes:
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    except ImportError as exc:
        raise RuntimeError("Install reportlab with: pip install reportlab") from exc

    output = BytesIO()
    document = SimpleDocTemplate(output, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("MindCare AI — Weekly Wellness Summary", styles["Title"]),
        Paragraph(f"Prepared for {username} on {datetime.now():%Y-%m-%d}", styles["Normal"]),
        Spacer(1, 16),
        Paragraph("This is a personal wellness summary, not a medical or diagnostic report.", styles["Italic"]),
        Spacer(1, 12),
        Table([["Metric", "Value"], ["Mood entries", str(len(moods))], ["Journal entries", str(len(journals))], ["Stored chat messages", str(message_count)]], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6366f1")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 7),
        ])),
        Spacer(1, 16),
        Paragraph("Mood history", styles["Heading2"]),
        Paragraph(", ".join(str(row[0]) for row in moods) or "No mood entries recorded.", styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("Journal highlights", styles["Heading2"]),
        Paragraph("Journal text is intentionally excluded to protect privacy. Review original entries directly with a trusted professional.", styles["BodyText"]),
    ]
    document.build(story)
    return output.getvalue()
