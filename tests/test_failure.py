# Tests for individual certificate failures
import sqlite3

from app.services import certificate_generator


def test_one_certificate_failure_does_not_stop_others(monkeypatch):
    db = sqlite3.connect("certificates.db")
    cursor = db.cursor()

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
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            "Failure Test Event",
            "ABC Technologies",
            "queued",
            3,
            0,
            0
        )
    )

    job_id = cursor.lastrowid

    recipients = [
        ("Rishi Raj", "rishi@example.com", "Python"),
        ("Rahul Kumar", "rahul@example.com", "Python"),
        ("Amit Sharma", "amit@example.com", "Python"),
    ]

    certificate_ids = []

    for name, email, course in recipients:
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
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            """,
            (
                job_id,
                name,
                email,
                course,
                "pending"
            )
        )

        certificate_ids.append(cursor.lastrowid)

    db.commit()
    db.close()

    original_create_certificate = certificate_generator.create_certificate

    def fake_create_certificate(
        certificate_id,
        recipient_name,
        course,
        event_name,
        organization
    ):
        if certificate_id == certificate_ids[1]:
            raise Exception("Simulated certificate generation failure")

        return original_create_certificate(
            certificate_id,
            recipient_name,
            course,
            event_name,
            organization
        )

    monkeypatch.setattr(
        certificate_generator,
        "create_certificate",
        fake_create_certificate
    )

    certificate_generator.process_job(job_id)

    db = sqlite3.connect("certificates.db")
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT status
        FROM certificates
        WHERE job_id = ?
        ORDER BY id
        """,
        (job_id,)
    )

    statuses = [row[0] for row in cursor.fetchall()]

    cursor.execute(
        """
        SELECT successful, failed, status
        FROM jobs
        WHERE id = ?
        """,
        (job_id,)
    )

    successful, failed, job_status = cursor.fetchone()

    db.close()

    assert statuses[0] == "completed"
    assert statuses[1] == "failed"
    assert statuses[2] == "completed"

    assert successful == 2
    assert failed == 1
    assert job_status == "completed_with_errors"