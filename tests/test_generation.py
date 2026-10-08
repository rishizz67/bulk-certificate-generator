# Tests for certificate generation
from pathlib import Path

from app.services.certificate_generator import create_certificate


def test_certificate_generation():
    output_path = create_certificate(
        certificate_id=999,
        recipient_name="Rishi Raj",
        course="Python Development",
        event_name="Python Workshop 2026",
        organization="ABC Technologies"
    )

    file_path = Path(output_path)

    assert file_path.exists()
    assert file_path.suffix == ".pdf"
    assert file_path.stat().st_size > 0