from datetime import datetime, timezone
import sqlite3

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlite3 import Connection

from app.database import get_db
from app.schemas import JobCreate, JobResponse
from app.services.certificate_generator import process_job


router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"]
)


@router.post("/", response_model=JobResponse)
def create_job(
    job_data: JobCreate,
    background_tasks: BackgroundTasks,
    db: Connection = Depends(get_db)
):
    created_at = datetime.now(timezone.utc).isoformat()

    cursor = db.cursor()

    # Create job
    cursor.execute(
        """
        INSERT INTO jobs (
            event_name,
            organization,
            status,
            total,
            successful,
            failed,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job_data.event_name,
            job_data.organization,
            "queued",
            len(job_data.recipients),
            0,
            0,
            created_at
        )
    )

    job_id = cursor.lastrowid

    # Create certificate records
    for recipient in job_data.recipients:
        cursor.execute(
            """
            INSERT INTO certificates (
                job_id,
                recipient_name,
                recipient_email,
                course,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                job_id,
                recipient.name,
                recipient.email,
                recipient.course,
                "pending",
                created_at
            )
        )

    db.commit()

    # Start background processing
    background_tasks.add_task(
        process_job,
        job_id
    )

    return {
        "job_id": job_id,
        "status": "queued",
        "total": len(job_data.recipients)
    }
@router.get("/{job_id}")
def get_job_status(
    job_id: int,
    db: Connection = Depends(get_db)
):
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT *
        FROM jobs
        WHERE id = ?
        """,
        (job_id,)
    )

    job = cursor.fetchone()

    if not job:
        return {
            "error": "Job not found"
        }

    total = job["total"]
    successful = job["successful"]
    failed = job["failed"]

    processed = successful + failed

    if total > 0:
        progress = round((processed / total) * 100, 2)
    else:
        progress = 0

    return {
        "job_id": job["id"],
        "status": job["status"],
        "event_name": job["event_name"],
        "organization": job["organization"],
        "total": total,
        "successful": successful,
        "failed": failed,
        "processed": processed,
        "progress": progress,
        "created_at": job["created_at"],
        "completed_at": job["completed_at"]
    }