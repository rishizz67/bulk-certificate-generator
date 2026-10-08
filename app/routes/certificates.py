import sqlite3
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlite3 import Connection

from app.database import get_db


router = APIRouter(
    prefix="/api/certificates",
    tags=["Certificates"]
)


@router.get("/{certificate_id}")
def get_certificate(
    certificate_id: int,
    db: Connection = Depends(get_db)
):
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT *
        FROM certificates
        WHERE id = ?
        """,
        (certificate_id,)
    )

    certificate = cursor.fetchone()

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    if certificate["status"] != "completed":
        raise HTTPException(
            status_code=404,
            detail="Certificate has not been generated yet"
        )

    file_path = certificate["file_path"]

    if not file_path:
        raise HTTPException(
            status_code=404,
            detail="Certificate file path not found"
        )

    if not Path(file_path).exists():
        raise HTTPException(
            status_code=404,
            detail="Certificate PDF file not found"
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"certificate_{certificate_id}.pdf"
    )