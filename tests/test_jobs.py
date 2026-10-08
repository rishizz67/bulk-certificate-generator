# Tests for creating generation jobs
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_generation_job():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Python Workshop 2026",
            "organization": "ABC Technologies",
            "recipients": [
                {
                    "name": "Rishi Raj",
                    "email": "rishi@example.com",
                    "course": "Python Development"
                },
                {
                    "name": "Rahul Kumar",
                    "email": "rahul@example.com",
                    "course": "Python Development"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["status"] == "queued"
    assert data["total"] == 2