# Predefined certificate template
from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas


def generate_certificate(
    recipient_name: str,
    course: str,
    event_name: str,
    organization: str,
    certificate_id: int,
    output_path: str
):
    """
    Generate a single PDF certificate.
    """

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    width, height = landscape(A4)

    pdf = canvas.Canvas(
        str(output_file),
        pagesize=(width, height)
    )

    # Background
    pdf.setFillColor(colors.white)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    # Outer border
    pdf.setStrokeColor(colors.HexColor("#1F4E79"))
    pdf.setLineWidth(5)
    pdf.rect(
        25,
        25,
        width - 50,
        height - 50,
        fill=0,
        stroke=1
    )

    # Inner border
    pdf.setStrokeColor(colors.HexColor("#D4AF37"))
    pdf.setLineWidth(2)
    pdf.rect(
        35,
        35,
        width - 70,
        height - 70,
        fill=0,
        stroke=1
    )

    # Title
    pdf.setFillColor(colors.HexColor("#1F4E79"))
    pdf.setFont("Helvetica-Bold", 30)

    pdf.drawCentredString(
        width / 2,
        height - 100,
        "CERTIFICATE OF PARTICIPATION"
    )

    # Subtitle
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 14)

    pdf.drawCentredString(
        width / 2,
        height - 135,
        "This certificate is proudly presented to"
    )

    # Recipient name
    pdf.setFillColor(colors.HexColor("#1F4E79"))
    pdf.setFont("Helvetica-Bold", 28)

    pdf.drawCentredString(
        width / 2,
        height - 190,
        recipient_name
    )

    # Description
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 13)

    pdf.drawCentredString(
        width / 2,
        height - 230,
        "for successfully participating in"
    )

    # Course
    pdf.setFillColor(colors.HexColor("#1F4E79"))
    pdf.setFont("Helvetica-Bold", 20)

    pdf.drawCentredString(
        width / 2,
        height - 265,
        course
    )

    # Event
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 12)

    pdf.drawCentredString(
        width / 2,
        height - 300,
        f"Event: {event_name}"
    )

    # Organization
    pdf.setFont("Helvetica-Bold", 13)

    pdf.drawCentredString(
        width / 2,
        height - 330,
        organization
    )

    # Date
    current_date = datetime.now().strftime("%d %B %Y")

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        70,
        75,
        f"Date: {current_date}"
    )

    # Certificate ID
    pdf.drawRightString(
        width - 70,
        75,
        f"Certificate ID: CERT-{certificate_id:05d}"
    )

    # Signature line
    pdf.line(
        width / 2 - 70,
        105,
        width / 2 + 70,
        105
    )

    pdf.setFont("Helvetica", 10)

    pdf.drawCentredString(
        width / 2,
        90,
        "Authorized Signature"
    )

    pdf.save()