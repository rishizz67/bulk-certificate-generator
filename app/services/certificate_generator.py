import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from templates.certificate_template import generate_certificate


GENERATED_DIR = Path("generated")
DATABASE_PATH = Path("certificates.db")


def create_certificate(
    certificate_id: int,
    recipient_name: str,
    course: str,
    event_name: str,
    organization: str
):
    GENERATED_DIR.mkdir(exist_ok=True)

    filename = f"certificate_{certificate_id}.pdf"
    output_path = GENERATED_DIR / filename

    generate_certificate(
        recipient_name=recipient_name,
        course=course,
        event_name=event_name,
        organization=organization,
        certificate_id=certificate_id,
        output_path=str(output_path)
    )

    return str(output_path)


def process_job(job_id: int):
    """
    Process every certificate belonging to a job.

    If one certificate fails, the remaining certificates
    continue processing.
    """

    db = sqlite3.connect(DATABASE_PATH)
    db.row_factory = sqlite3.Row

    try:
        cursor = db.cursor()

        # Mark job as processing
        cursor.execute(
            """
            UPDATE jobs
            SET status = ?
            WHERE id = ?
            """,
            ("processing", job_id)
        )

        db.commit()

        # Get job information
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
            return

        # Get all certificates belonging to this job
        cursor.execute(
            """
            SELECT *
            FROM certificates
            WHERE job_id = ?
            """,
            (job_id,)
        )

        certificates = cursor.fetchall()

        successful = 0
        failed = 0

        for certificate in certificates:

            try:
                # Mark individual certificate as processing
                cursor.execute(
                    """
                    UPDATE certificates
                    SET status = ?
                    WHERE id = ?
                    """,
                    ("processing", certificate["id"])
                )

                db.commit()

                # Generate PDF
                file_path = create_certificate(
                    certificate_id=certificate["id"],
                    recipient_name=certificate["recipient_name"],
                    course=certificate["course"],
                    event_name=job["event_name"],
                    organization=job["organization"]
                )

                # Mark certificate as successful
                cursor.execute(
                    """
                    UPDATE certificates
                    SET status = ?,
                        file_path = ?
                    WHERE id = ?
                    """,
                    (
                        "completed",
                        file_path,
                        certificate["id"]
                    )
                )

                successful += 1

            except Exception as error:

                # One certificate failed.
                # Continue processing the remaining certificates.
                cursor.execute(
                    """
                    UPDATE certificates
                    SET status = ?,
                        error_message = ?
                    WHERE id = ?
                    """,
                    (
                        "failed",
                        str(error),
                        certificate["id"]
                    )
                )

                failed += 1

            db.commit()

        # Determine final job status
        if failed == 0:
            final_status = "completed"
        else:
            final_status = "completed_with_errors"

        completed_at = datetime.now(timezone.utc).isoformat()

        cursor.execute(
            """
            UPDATE jobs
            SET status = ?,
                successful = ?,
                failed = ?,
                completed_at = ?
            WHERE id = ?
            """,
            (
                final_status,
                successful,
                failed,
                completed_at,
                job_id
            )
        )

        db.commit()

    except Exception as error:

        cursor.execute(
            """
            UPDATE jobs
            SET status = ?
            WHERE id = ?
            """,
            ("failed", job_id)
        )

        db.commit()

    finally:
        db.close()