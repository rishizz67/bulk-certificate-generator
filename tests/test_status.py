# Tests for job status/progress
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_job_status_and_progress():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Status Test Event",
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

    job_id = response.json()["job_id"]

    status_response = client.get(f"/api/jobs/{job_id}")

    assert status_response.status_code == 200

    data = status_response.json()

    assert data["job_id"] == job_id
    assert data["total"] == 2
    assert "successful" in data
    assert "failed" in data
    assert "processed" in data
    assert "progress" in data
    assert 0 <= data["progress"] <= 100